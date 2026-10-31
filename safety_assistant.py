def get_safety_advice(question):

    question = question.lower()

    if "otp" in question or "pin" in question:
        return {
            "topic": "OTP and PIN Safety",
            "advice": "Never share your OTP, UPI PIN or bank PIN with anyone.",
            "status": "Safety Advice"
        }

    elif "upi" in question or "payment" in question:
        return {
            "topic": "UPI Safety",
            "advice": "Check the receiver name before making a payment. Never approve unknown collect requests.",
            "status": "Safety Advice"
        }

    elif "link" in question or "website" in question:
        return {
            "topic": "Link Safety",
            "advice": "Avoid unknown links. Never enter bank details on untrusted websites.",
            "status": "Safety Advice"
        }

    elif "bank" in question:
        return {
            "topic": "Bank Safety",
            "advice": "Never share banking details with unknown callers. Contact your bank through official channels.",
            "status": "Safety Advice"
        }

    else:
        return {
            "topic": "General Safety",
            "advice": "Stay alert. Never share personal information or make payments to unknown people.",
            "status": "Safety Advice"
        }