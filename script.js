
let totalChecks = 0;
let totalWarnings = 0;
let safeChecks = 0;

const $ = (id) => document.getElementById(id);

function updateStats() {
  $("totalChecks").textContent = totalChecks;
  $("totalWarnings").textContent = totalWarnings;
  $("safeChecks").textContent = safeChecks;
}

function showResult(id, message, isWarning) {
  const box = $(id);
  box.textContent = message;
  box.className = "result-box show " + (isWarning ? "warning" : "safe");
}

function addAlert(title, detail) {
  const list = $("alertList");
  const empty = list.querySelector(".empty-state");
  if (empty) empty.remove();

  const item = document.createElement("div");
  item.className = "alert-item";

  const heading = document.createElement("strong");
  heading.textContent = title;

  const description = document.createElement("div");
  description.textContent = detail;

  const time = document.createElement("small");
  time.textContent = new Date().toLocaleTimeString();

  item.append(heading, description, time);
  list.prepend(item);
}

const suspiciousWords = [
  "urgent", "account blocked", "verify your account",
  "prize", "winner", "send otp", "share otp",
  "bank details", "click here", "kyc update",
  "claim now", "limited time", "password",
  "upi pin", "refund", "lottery", "free gift"
];

$("checkMessageBtn").addEventListener("click", () => {
  const message = $("messageInput").value.trim().toLowerCase();

  if (!message) {
    showResult("messageResult", "Please paste a message first.", true);
    return;
  }

  totalChecks++;

  const found = suspiciousWords.filter(word => message.includes(word));
  const hasLink = /(https?:\/\/|www\.)/i.test(message);
  const hasMoneyPressure = /(pay now|transfer money|send money)/i.test(message);

  const warning = found.length > 0 || hasLink || hasMoneyPressure;

  if (warning) {
    totalWarnings++;
    const reasons = [];
    if (found.length) reasons.push("Suspicious words: " + found.join(", "));
    if (hasLink) reasons.push("Contains a website link.");
    if (hasMoneyPressure) reasons.push("Contains a payment request.");

    showResult(
      "messageResult",
      "⚠ Potential warning signs found. " + reasons.join(" ") +
      " Do not share OTP, PIN or bank details. Verify independently.",
      true
    );
    addAlert("Suspicious message warning", "Potential risk indicators found in a message.");
  } else {
    safeChecks++;
    showResult(
      "messageResult",
      "✓ No obvious warning signs found by this basic check. This does NOT guarantee the message is genuine.",
      false
    );
    addAlert("Message checked", "No obvious warning signs detected.");
  }

  updateStats();
});

$("checkLinkBtn").addEventListener("click", () => {
  const raw = $("urlInput").value.trim();

  if (!raw) {
    showResult("linkResult", "Please enter a website link first.", true);
    return;
  }

  totalChecks++;

  let warningReasons = [];
  let parsedURL;

  try {
    parsedURL = new URL(/^https?:\/\//i.test(raw) ? raw : "https://" + raw);

    if (!["http:", "https:"].includes(parsedURL.protocol)) {
      warningReasons.push("Unexpected web protocol.");
    }

    if (parsedURL.username || parsedURL.password) {
      warningReasons.push("Link contains embedded login credentials.");
    }

    if (parsedURL.hostname.startsWith("xn--")) {
      warningReasons.push("Domain uses encoded characters.");
    }

    if (/^\d{1,3}(\.\d{1,3}){3}$/.test(parsedURL.hostname)) {
      warningReasons.push("Link uses an IP address instead of a normal domain.");
    }

    if (["bit.ly", "tinyurl.com", "t.co", "cutt.ly", "is.gd"].includes(parsedURL.hostname.toLowerCase())) {
      warningReasons.push("Shortened link hides the final destination.");
    }

    if (parsedURL.hostname.split(".").length > 4) {
      warningReasons.push("Unusually many subdomains.");
    }

    if (parsedURL.protocol !== "https:") {
      warningReasons.push("The link does not use HTTPS.");
    }
  } catch {
    warningReasons.push("The link format could not be recognised.");
  }

  if (warningReasons.length > 0) {
    totalWarnings++;
    showResult(
      "linkResult",
      "⚠ Caution: " + warningReasons.join(" ") +
      " Do not open the link or enter personal information until independently verified.",
      true
    );
    addAlert("Link warning", "Potentially suspicious link indicators found.");
  } else {
    safeChecks++;
    showResult(
      "linkResult",
      "✓ No obvious technical warning signs found. This basic check cannot confirm that a website is safe. Verify the domain independently.",
      false
    );
    addAlert("Link checked", "No obvious warning indicators detected.");
  }

  updateStats();
});

$("clearAlerts").addEventListener("click", () => {
  $("alertList").innerHTML =
    '<div class="empty-state"><span>✓</span><p>No alerts yet. Your checks will appear here.</p></div>';
});

const replies = [
  {
    words: ["otp", "pin", "password"],
    answer: "Never share your OTP, UPI PIN or password with anyone. Banks do not ask you to reveal these secrets over calls or messages."
  },
  {
    words: ["upi", "payment", "refund", "money"],
    answer: "Be careful with UPI collect requests. You generally do not need to enter your UPI PIN to receive money. Verify every payment request."
  },
  {
    words: ["link", "website", "url"],
    answer: "Check the website address carefully. Avoid unknown shortened links and never enter personal details on an unverified website."
  },
  {
    words: ["sms", "message", "whatsapp", "scam"],
    answer: "Be cautious of urgent messages, unexpected prizes and requests for money or personal information. Verify through official channels."
  }
];

function getAssistantReply(question) {
  const text = question.toLowerCase();
  const match = replies.find(item => item.words.some(word => text.includes(word)));

  if (match) return match.answer;

  return "Stay alert online. Never share your OTP, UPI PIN or passwords. Do not trust unknown links or unexpected payment requests. Contact your bank through its official number if you suspect fraud.";
}

function addChatMessage(message, type) {
  const bubble = document.createElement("div");
  bubble.className = type === "user" ? "user-message" : "bot-message";
  bubble.textContent = message;
  $("chatMessages").appendChild(bubble);
  $("chatMessages").scrollTop = $("chatMessages").scrollHeight;
}

$("chatForm").addEventListener("submit", (event) => {
  event.preventDefault();

  const input = $("chatInput");
  const question = input.value.trim();

  if (!question) return;

  addChatMessage(question, "user");
  input.value = "";

  addChatMessage(getAssistantReply(question), "bot");
});

// Language selector
const translations = {
  en: {
    pageTitle: "Security Dashboard",
    welcome: "Welcome to CYBERKAVACH",
    subtitle: "Think Smart. Stay Protected. Take control of your digital safety.",
    message: "Scam Message Checker",
    link: "Fake Link Checker",
    alerts: "Recent Security Alerts",
    assistant: "Safety Assistant"
  },
  hi: {
    pageTitle: "सुरक्षा डैशबोर्ड",
    welcome: "CYBERKAVACH में आपका स्वागत है",
    subtitle: "समझदारी से सोचें। सुरक्षित रहें। अपनी डिजिटल सुरक्षा का ध्यान रखें।",
    message: "संदिग्ध संदेश जांचें",
    link: "फर्जी लिंक जांचें",
    alerts: "हाल की सुरक्षा चेतावनियां",
    assistant: "सुरक्षा सहायक"
  },
  pa: {
    pageTitle: "ਸੁਰੱਖਿਆ ਡੈਸ਼ਬੋਰਡ",
    welcome: "CYBERKAVACH ਵਿੱਚ ਤੁਹਾਡਾ ਸਵਾਗਤ ਹੈ",
    subtitle: "ਸਮਝਦਾਰੀ ਨਾਲ ਸੋਚੋ। ਸੁਰੱਖਿਅਤ ਰਹੋ। ਆਪਣੀ ਡਿਜੀਟਲ ਸੁਰੱਖਿਆ ਦਾ ਧਿਆਨ ਰੱਖੋ।",
    message: "ਸ਼ੱਕੀ ਸੁਨੇਹਾ ਜਾਂਚੋ",
    link: "ਨਕਲੀ ਲਿੰਕ ਜਾਂਚੋ",
    alerts: "ਹਾਲੀਆ ਸੁਰੱਖਿਆ ਚੇਤਾਵਨੀਆਂ",
    assistant: "ਸੁਰੱਖਿਆ ਸਹਾਇਕ"
  }
};

$("languageSelect").addEventListener("change", (event) => {
  const lang = translations[event.target.value];

  $("pageTitle").textContent = lang.pageTitle;
  document.querySelector(".welcome-banner h2").textContent = lang.welcome;
  document.querySelector(".welcome-banner p").textContent = lang.subtitle;
  document.querySelector("#message-checker h3").textContent = lang.message;
  document.querySelector("#link-checker h3").textContent = lang.link;
  document.querySelector("#alerts h2").textContent = lang.alerts;
  document.querySelector("#assistant h2").textContent = lang.assistant;
});

updateStats();
