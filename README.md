# TELEGRAM BOT 'GOOGLE CALENDAR - NOTION'

🤖 Telegram Startup Assistant
Assistant personnel connecté à OpenAI, Notion, Google Calendar et SMTP, destiné à accompagner un solo-preneur dans ses tâches quotidiennes : mailing, gestion de rendez-vous, et réponses IA personnalisées.

📦 Fonctionnalités
✅ Commandes Telegram
/start – Affiche les instructions d’utilisation

/mailing – Prévisualise un envoi d’e-mails basé sur les données de Notion

/confirm – Envoie les mails aux prospects listés

/list – Liste les événements restants aujourd’hui dans Google Calendar

Texte libre – Gère automatiquement :

📅 Création/suppression d’événements

🤖 Réponses IA OpenAI

✉️ Gestion intelligente du mailing

🔌 Intégrations
OpenAI (GPT-4o) – Réponses IA, extraction d’événements en langage naturel

Google Calendar API – Création, suppression, affichage d’événements

Notion API – Récupération de prospects pour les campagnes mails

SMTP – Envoi de mails personnalisés (templating HTML)

Telegram Bot – Interface utilisateur via l'app Telegram

🧾 Structure des dossiers
bash
Copier
Modifier
project-root/
│
├── google_calendar/
│   └── google_calendar.py            # Fonctions pour interagir avec Google Calendar
│
├── google_notion_mailing/
│   ├── mailer.py                     # Fonction d'envoi de mail
│   ├── email_utils.py                # Templating HTML
│   └── notion_utils.py               # Extraction des prospects
│
├── main.py                           # Script principal du bot
├── .env                              # Clés API et tokens
└── README.md                         # Ce fichier

⚙️ Prérequis
Python 3.10+

Un bot Telegram actif avec TELEGRAM_TOKEN

Une clé API OpenAI : OPENAI_API_KEY

Accès aux APIs :

Notion

Google Calendar

SMTP pour l’envoi d’emails

🛠️ Installation
bash
Copier
Modifier

# 1. Cloner le repo
git clone https://github.com/cerealmilkdev/MS_BOT_OPENAI_TELEGRAM.git
cd startup-assistant

# 3. Configurer les variables d'environnement
cp .env.example .env
puis remplir avec :
TELEGRAM_TOKEN=...
OPENAI_API_KEY=...

# 4. Lancer le bot
python main.py

🔐 Fichier .env attendu
dotenv
Copier
Modifier

TELEGRAM_TOKEN=your_telegram_bot_token

OPENAI_API_KEY=your_openai_api_key

EMAIL_HOST=smtp.example.com

EMAIL_PORT=587

EMAIL_USERNAME=your_email@example.com

EMAIL_PASSWORD=your_email_password

NOTION_TOKEN=your_notion_token

NOTION_DATABASE_ID=your_database_id

# 🚀 Exemple d’usage

Envoyer "ajoutes un rdv demain à 14h avec Alex sur Telegram" ➜ le bot crée un événement dans Google Calendar

Envoyer /mailing ➜ le bot récupère les prospects Notion, affiche un aperçu, puis /confirm envoie les mails automatiquement

Envoyer un message libre ➜ le bot répond via GPT-4o de manière concise et professionnelle

📌 À venir

Tracking de réponses aux e-mails

Intégration CRM (HubSpot / Airtable / n8n)
🧠 Contributeurs
Conçu pour les fondateurs solo, no-code users et développeurs cherchant à automatiser leur stack startup.
