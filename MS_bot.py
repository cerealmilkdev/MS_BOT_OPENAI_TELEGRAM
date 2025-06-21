import os
import logging
import asyncio
import pytz
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler, MessageHandler, filters
from openai import OpenAI

from google_notion_mailing.email_utils import render_template
from google_notion_mailing.notion_utils import get_prospects_from_notion
from google_notion_mailing.mailer import send_mail
from google_calendar.google_calendar import get_calendar_service, add_event, delete_event_by_summary, get_todays_events

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)
pending_mailing = {}

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# === DISPATCHER INTELLIGENT POUR LES MESSAGES TEXTES ===
async def unified_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    calendar_keywords = ["rendez-vous", "rdv", "ajoutes", "planifie", "event", "modifie event", "supprime event"]

    if any(k in text for k in calendar_keywords):
        await smart_calendar_handler(update, context)
    else:
        await ia_agent(update, context)

# === HANDLERS ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bienvenue ! Commandes disponibles :\n"
        "/mailing - Envoie de mails aux prospects Notion\n"
        "/list - Affiche les événements restants aujourd'hui\n"
        "Tu peux aussi écrire directement : 'ajoute un événement demain à 14h'"
    )

async def ia_agent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = update.message.text
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Tu es un assistant professionnel, concis, qui répond uniquement à la demande, sans bavardage."},
            {"role": "user", "content": question}
        ]
    )
    await update.message.reply_text(response.choices[0].message.content)

async def mailing_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    prospects = get_prospects_from_notion()
    if not prospects:
        await update.message.reply_text("📭 Aucun prospect à contacter.")
        return

    preview = render_template(prospects[0])
    pending_mailing[user_id] = prospects
    await update.message.reply_text(
        f"{len(prospects)} mails seront envoyés. Aperçu :\n\n{preview[:1000]}\n\n"
        "✅ Tape /confirm pour envoyer ou /annuler pour annuler."
    )

async def confirm_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    prospects = pending_mailing.pop(user_id, None)
    if not prospects:
        await update.message.reply_text("⚠️ Aucun envoi en attente.")
        return

    await update.message.reply_text("📤 Envoi des mails...")
    for prospect in prospects:
        html = render_template(prospect)
        send_mail(to=prospect['email'], subject="Découvrez MakeSocial", html=html)
        await asyncio.sleep(2)
    await update.message.reply_text("✅ Tous les mails ont été envoyés.")

# === SMART CALENDAR HANDLER ===
async def smart_calendar_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower()
    today_str = datetime.now(pytz.timezone("America/Toronto")).strftime("%Y-%m-%d")
    keywords_create = ["rendez-vous", "rdv", "ajoute", "planifie", "event"]

    if any(k in user_text for k in keywords_create):
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system",
                     "content":
                    f"Aujourd'hui, nous sommes le {today_str}. Tu es un assistant Google Calendar. "
                    "Tu dois extraire les informations de création d’un événement à partir d’un message. "
                    "Tu dois répondre STRICTEMENT en JSON brut, sans aucune explication, sans balise, sans introduction, sans texte autour. "
                    "Format OBLIGATOIRE : {\"title\": \"...\", \"start\": \"YYYY-MM-DDTHH:MM:SS\", \"end\": \"YYYY-MM-DDTHH:MM:SS\", \"description\": \"...\"}. "
                    "Si les données sont incomplètes, retourne simplement {}."},
                    {"role": "user", "content": user_text}
                ]
            )
            content = response.choices[0].message.content.strip()
            print(f"📥 Réponse brute GPT:\n{content}")
            data = json.loads(response.choices[0].message.content)
            start = pytz.timezone("America/Toronto").localize(datetime.fromisoformat(data['start']))
            end = pytz.timezone("America/Toronto").localize(datetime.fromisoformat(data['end']))
            event = add_event(data['title'], data.get('description', ''), start, end)
            await update.message.reply_text(f"✅ Événement créé : {event.get('htmlLink')}")
        except Exception as e:
            await update.message.reply_text(f"⚠️ Erreur lors de la création : {e}")

    elif "supprime event" in user_text:
        try:
            title = user_text.split("supprime event")[-1].strip()
            success = delete_event_by_summary(title)
            if success:
                await update.message.reply_text(f"🗑️ Événement '{title}' supprimé.")
            else:
                await update.message.reply_text("❓ Aucun événement trouvé avec ce titre.")
        except Exception as e:
            await update.message.reply_text(f"❌ Erreur : {e}")

    elif "modifie event" in user_text:
        try:
            title = user_text.split("modifie event")[-1].strip()
            await update.message.reply_text(f"🔎 Recherche de l’événement à modifier : '{title}' (fonction à implémenter pour modification précise)")
            # Tu peux ici lister l'événement et proposer une récréation
        except Exception as e:
            await update.message.reply_text(f"❌ Erreur : {e}")

# === COMMANDE LIST ===
async def list_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        events = get_todays_events()
        now = datetime.now(pytz.timezone("America/Toronto"))
        filtered = []
        for e in events:
            start_str = e['start'].get('dateTime')
            if start_str:
                start_dt = datetime.fromisoformat(start_str).astimezone(pytz.timezone("America/Toronto"))
                if start_dt > now:
                    filtered.append((start_dt.strftime("%H:%M"), e.get('summary', 'Sans titre')))

        if not filtered:
            await update.message.reply_text("📭 Aucun événement restant aujourd'hui.")
        else:
            msg = "📅 Événements restants aujourd'hui :\n\n"
            msg += "\n".join([f"🕒 {h} - {t}" for h, t in filtered])
            await update.message.reply_text(msg)
    except Exception as e:
        await update.message.reply_text(f"❌ Erreur : {e}")

# === MAIN ===
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("mailing", mailing_handler))
    app.add_handler(CommandHandler("confirm", confirm_handler))
    app.add_handler(CommandHandler("list", list_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unified_message_handler))
    app.run_polling()

if __name__ == "__main__":
    main()
