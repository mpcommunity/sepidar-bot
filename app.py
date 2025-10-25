from flask import Flask, request
import requests

app = Flask(__name__)

# توکن ربات بله
BALE_TOKEN = "350738185:7ximMRHSFkjUttN0jDRYxa01U1fgeDbyrgk"

# تابع ارسال پیام
def send_message(chat_id, text):
    url = f"https://tapi.bale.ai/bot{BALE_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    chat_id = data["message"]["chat"]["id"]
    text = data["message"]["text"]

    if text == "/start":
        send_message(chat_id, "سلام 👋 خوش اومدی به ربات ساده‌ی من!")

    return "ok"
