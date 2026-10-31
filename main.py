
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import re

from link_checker import analyze_link
from safety_assistant import get_safety_advice
from database import create_table, save_alert, read_alerts as get_saved_alerts


app = FastAPI(title="ScamShield Backend")


# CORS Settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create database table
create_table()


# Home API
@app.get("/")
def home():
    return {
        "message": "ScamShield Backend is Running!",
        "status": "success"
    }


# Health API
@app.get("/health")
def health():
    return {"status": "healthy"}


# Message Checker
class MessageInput(BaseModel):
    message: str


@app.post("/check-message")
def check_message(data: MessageInput):

    message = data.message.lower()
    risk_score = 0
    reasons = []

    patterns = [
        (r"\botp\b", "Message mentions OTP"),
        (r"\bpin\b", "Message asks about PIN"),
        (r"\bpassword\b", "Message mentions password"),
        (r"urgent|immediately|act now", "Creates urgency"),
        (r"lottery|prize|winner|reward", "Possible fake reward offer"),
        (r"bank account|account blocked", "Possible bank impersonation"),
        (r"send money|pay now|transfer money", "Requests payment"),
        (r"click here|verify now", "Pressures user to take action")
    ]

    for pattern, reason in patterns:
        if re.search(pattern, message):
            risk_score += 20
            reasons.append(reason)

    if re.search(r"https?://|www\.", message):
        risk_score += 20
        reasons.append("Contains a web link")

    risk_score = min(risk_score, 100)

    if risk_score >= 60:
        status = "High Risk"
    elif risk_score >= 20:
        status = "Suspicious"
    else:
        status = "Low Risk"

    return {
        "status": status,
        "risk_score": risk_score,
        "reasons": reasons,
        "message": "Message analysis completed"
    }


# Fake Link Checker
class LinkInput(BaseModel):
    url: str


@app.post("/check-link")
def check_link(data: LinkInput):
    return analyze_link(data.url)


# Scam Alerts
class AlertInput(BaseModel):
    title: str
    category: str
    description: str
    severity: str


@app.get("/alerts")
def read_alerts():
    return get_saved_alerts()


@app.post("/alerts")
def create_alert(data: AlertInput):

    alert_date = datetime.now().isoformat()

    alert_id = save_alert(
        data.title,
        data.category,
        data.description,
        data.severity,
        alert_date
    )

    return {
        "id": alert_id,
        "title": data.title,
        "category": data.category,
        "description": data.description,
        "severity": data.severity,
        "date": alert_date
    }


# Safety Assistant
class SafetyInput(BaseModel):
    question: str


@app.post("/safety-assistant")
def safety_assistant(data: SafetyInput):
    return get_safety_advice(data.question)
