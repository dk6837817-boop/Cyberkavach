
from datetime import datetime

# Scam alerts storage
scam_alerts = [
    {
        "id": 1,
        "title": "Fake UPI Payment Message",
        "category": "UPI Fraud",
        "description": "Scammers may send fake payment confirmation messages.",
        "severity": "High",
        "date": datetime.now().isoformat()
    },
    {
        "id": 2,
        "title": "Fake Bank KYC Link",
        "category": "Phishing",
        "description": "Be careful of unknown links asking for bank KYC details.",
        "severity": "High",
        "date": datetime.now().isoformat()
    },
    {
        "id": 3,
        "title": "Online Shopping Scam",
        "category": "Shopping Fraud",
        "description": "Avoid paying unknown sellers without verifying them.",
        "severity": "Medium",
        "date": datetime.now().isoformat()
    }
]


def get_alerts():
    return scam_alerts


def add_alert(title, category, description, severity):

    new_alert = {
        "id": max([a["id"] for a in scam_alerts], default=0) + 1,
        "title": title,
        "category": category,
        "description": description,
        "severity": severity,
        "date": datetime.now().isoformat()
    }

    scam_alerts.append(new_alert)

    return new_alert
