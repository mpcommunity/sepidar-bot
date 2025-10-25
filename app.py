import os
import requests
from flask import Flask, request

app = Flask(__name__)

# گرفتن توکن از محیط
BALE_TOKEN = os.environ.get("350738185:7ximMRHSFkjUttN0jDRYxa01U1fgeDbyrgk")

# تابع ارسال پیام به بله
def send_message(chat_id, text):
    url = f"https://tapi.bale.ai/bot{BALE_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

# دریافت پیام از بله
@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    message = data.get("message", {})
    chat = message.get("chat", {})
    chat_id = chat.get("id")
    user_text = message.get("text", "")

    if not chat_id or not user_text:
        return "invalid", 400

    # فقط به /start جواب بده
    if user_text == "/start":
        welcome = "سلام 👋\nبه ربات ائتلاف سپیدار خوش اومدی! 🌿\nهر سوالی درباره نمایشگاه پژوهشی داری بپرس! 🧠"
        send_message(chat_id, welcome)

    return "ok"

# اجرای Flask برای Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
