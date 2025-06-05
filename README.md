🤖 Bot Telegram IA –  MakeSocial_Bot
Ce projet est un bot Telegram alimenté par l'API OpenAI (GPT-4o), conçu pour répondre automatiquement et efficacement aux messages des utilisateurs avec un ton professionnel et concis.

📦 Fonctionnalités
Commande /start pour accueillir l’utilisateur.

Traitement de tout message texte via GPT-4o.

Réponses directes, sans fioritures ni bavardage.

Intégration simple avec la librairie python-telegram-bot.

🚀 Installation
1. Cloner le dépôt
bash
Copier
Modifier
git clone https://github.com/ton-utilisateur/ton-repo.git
cd ton-repo
2. Créer un environnement virtuel (optionnel mais recommandé)
bash
Copier
Modifier
python -m venv venv
source venv/bin/activate  # Sous Windows : venv\Scripts\activate
3. Installer les dépendances
bash
Copier
Modifier
pip install -r requirements.txt
Exemple de requirements.txt à créer :

Copier
Modifier
python-telegram-bot~=20.0
openai
python-dotenv
4. Ajouter les variables d’environnement
Créer un fichier .env à la racine du projet avec le contenu suivant :

ini
Copier
Modifier
TELEGRAM_TOKEN=ton_token_telegram
OPENAI_API_KEY=ta_clef_openai
⚙️ Lancer le bot
bash
Copier
Modifier
python bot.py
🧠 Architecture
bot.py : Point d’entrée du bot Telegram.

agents.py : (à créer ou compléter) contient la classe Agent (non utilisée dans ce script mais importée).

.env : Stocke les secrets d’API.

🛡️ Bonnes pratiques
Ne jamais exposer .env dans les commits publics.

Respecter la politique d’utilisation d’OpenAI et Telegram.

Prévoir un système de logs avancé en production.

📜 Licence
MIT – libre d’utilisation, modification, distribution avec mention de l’auteur.

