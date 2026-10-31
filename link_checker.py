
from urllib.parse import urlparse
import re
import ipaddress

def analyze_link(url):

    risk_score = 0
    reasons = []

    url = url.strip()

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)
    domain = parsed.hostname or ""

    if not domain:
        return {
            "status": "Invalid URL",
            "risk_score": 0,
            "reasons": ["URL is not valid"]
        }

    # Check HTTP connection
    if parsed.scheme == "http":
        risk_score += 20
        reasons.append("Website does not use HTTPS")

    # Check IP address
    try:
        ipaddress.ip_address(domain)
        risk_score += 30
        reasons.append("Website uses an IP address")
    except ValueError:
        pass

    # Check shortened links
    short_domains = [
        "bit.ly", "tinyurl.com", "t.co",
        "is.gd", "cutt.ly"
    ]

    if domain.lower() in short_domains:
        risk_score += 30
        reasons.append("Shortened URL hides the destination")

    # Check suspicious words
    suspicious_words = [
        "login", "verify", "password",
        "banking", "account", "update",
        "free", "reward", "wallet"
    ]

    for word in suspicious_words:
        if word in url.lower():
            risk_score += 10
            reasons.append(f"Suspicious keyword: {word}")

    # Check unusual URL characters
    if "@" in url:
        risk_score += 30
        reasons.append("URL contains an unusual @ symbol")

    risk_score = min(risk_score, 100)

    if risk_score >= 60:
        status = "High Risk"
    elif risk_score >= 20:
        status = "Suspicious"
    else:
        status = "Low Risk"

    return {
        "url": url,
        "status": status,
        "risk_score": risk_score,
        "reasons": reasons,
        "message": "Link analysis completed"
    }
