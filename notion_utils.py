import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()
notion = Client(auth=os.getenv("NOTION_TOKEN"))
DATABASE_ID = os.getenv("NOTION_DB_ID")

def get_prospects_from_notion():
    results = notion.databases.query(
        **{
            "database_id": DATABASE_ID,
            "filter": {
                "and": [
                    {
                        "property": "Statut",
                        "status": {
                            "equals": "À envoyer"
                        }
                    },
                    {
                        "property": "Email",
                        "email": {
                            "is_not_empty": True
                        }
                    }

                ]

            }
        }
    ).get("results", [])

    prospects = []
    for row in results:
        email = row["properties"]["Email"]["email"]
        nom = row["properties"]["Nom"]["title"][0]["plain_text"]
        prospects.append({
            "email": email,
            "nom": nom,
            "notion_id": row["id"]
        })
    return prospects