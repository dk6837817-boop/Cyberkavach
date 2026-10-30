
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="CYBERKAVACH API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MessageRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"message": "Welcome to CYBERKAVACH Backend!"}

@app.get("/status")
def status():
    return {"project": "CYBERKAVACH", "status": "Active"}

@app.post("/check-message")
def check_message(data: MessageRequest):
    suspicious_words = [
        "otp", "account blocked", "verify your account",
        "upi pin", "bank details", "claim prize",
        "send money", "password", "urgent"
    ]

    message = data.message.lower()

    found_words = [
        word for word in suspicious_words
        if word in message
    ]

    if found_words:
        return {
            "result": "Suspicious",
            "warning": "This message contains suspicious words.",
            "matched_words": found_words
        }

    return {
        "result": "No obvious warning signs",
        "warning": "This does not guarantee that the message is safe.",
        "matched_words": []
    }