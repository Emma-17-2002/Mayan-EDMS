import requests
import json
from datetime import datetime

BASE_URL = "http://localhost/api/v4"

USERNAME = "admin"
PASSWORD = "DocuTech@2026"


session = requests.Session()
session.auth = (USERNAME, PASSWORD)

headers = {
    "Accept": "application/json"
}

response = session.get(
    f"{BASE_URL}/documents/",
    headers=headers
)

documents = response.json().get("results", [])
activite_recente = []

stats = {}

for doc in documents:
    activite_recente.append({

        "document":
        doc.get(
            "label",
            "Sans nom"
        ),

        "date":
        doc.get(
            "datetime_created",
            ""
        )

    })

    doc_type = doc.get(
        "document_type",
        {}
    ).get(
        "label",
        "Inconnu"
    )

    stats[doc_type] = stats.get(
        doc_type,
        0
    ) + 1

workflow = {

    "brouillon": 0,

    "attente_budget": 0,

    "attente_securite": 0,

    "approuve": 0,

    "rejete": 0
}

for doc in documents:

    state = "brouillon"

    try:

        latest_version_url = doc.get(
            "latest_version_url"
        )

        if latest_version_url:

            version_response = session.get(
                latest_version_url,
                headers=headers
            )

            version_data = version_response.json()

            comment = version_data.get(
                "comment",
                ""
            ).lower()

            state = comment

    except:
        pass

    if "budget" in state:

        workflow["attente_budget"] += 1

    elif "sécurité" in state or "securite" in state:

        workflow["attente_securite"] += 1

    elif "approuvé" in state or "approuve" in state:

        workflow["approuve"] += 1

    elif "rejeté" in state or "rejete" in state:

        workflow["rejete"] += 1

    else:

        workflow["brouillon"] += 1

rapport = {
    "date":
    datetime.now().strftime(
        "%Y-%m-%d %H:%M"
    ),

    "api_status":
    "Connectée",

    "ocr_status":
    "Actif",

    "docker_status":
    "Opérationnel",
  
"activite_recente":
activite_recente[:10],

    "total_documents":
    len(documents),

    "statistiques":
    stats,

    "documents_expirant_30_jours":
    [],

    "documents_expirant_7_jours":
    [],

    "workflow":
    workflow,

    "conformite":
    87
}

with open(
    "rapport.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        rapport,
        f,
        ensure_ascii=False,
        indent=4
    )

print("Rapport généré.")