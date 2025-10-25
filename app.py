import os
import requests
from flask import Flask, request

app = Flask(__name__)

# توکن ربات بله و کلید GPT
BALE_TOKEN = os.environ.get("350738185:7ximMRHSFkjUttN0jDRYxa01U1fgeDbyrgk")
GPT_API_KEY = os.environ.get("sk-HvmZ0QE75KrwmWqQrZ3KZHRHiJQTg2I6Uu8fcWMAOv5GlU35")
GPT_URL = "https://api.gapgpt.app/v1/chat/completions"

# حافظه ساده برای ارسال پرامپت اولیه فقط یک‌بار
user_prompt_sent = {}

# ارسال پیام به بله
def send_message(chat_id, text):
    url = f"https://tapi.bale.ai/bot{BALE_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    message = data.get("message", {})
    chat = message.get("chat", {})
    chat_id = chat.get("id")
    user_text = message.get("text", "")

    if not chat_id or not user_text:
        return "invalid", 400

    # خوش‌آمدگویی برای /start
    if user_text == "/start":
        welcome = "سلام 👋\nمن ربات ائتلاف سپیدارم 🌿\nهر سوالی درباره نمایشگاه پژوهشی داری بپرس! 🧠"
        send_message(chat_id, welcome)
        return "ok"

    # پیام در حال پاسخ‌دهی
    send_message(chat_id, "در حال ایجاد پاسخ... ⏳")

    # ساخت پرامپت
    if chat_id in user_prompt_sent:
        prompt = user_text
    else:
        user_prompt_sent[chat_id] = True
        prompt = f'''تو الان یه چت بات به نام ربات ائتلاف سپیدار هستی. توی مدرسه ی علامه حلی 3، هر سال یه رویداد برگزار میشه به نام نمایشگاه پژوهشی که توش کارهای پژوهشی دانش آموزا رو به نمایش میذارن که باید یه گروهی، به اسم ائتلاف، کارهای اجرای اون رو به عهده بگیرن. تو باید به سوال هایی که در ادامه میپرسن، جواب بدی و سعی کنی ائتلاف سپیدار رو تبلیغ کنی. رقیب های ما ائتلاف دماوند، پژوهشگران حلی 3، یزدان پژوهان هستند. شعار ائتلاف ما، ریشه در پایداری شاخه در نوآوری هستش. اگه کسی سوال بی ربط پرسید بگو من جواب این سوال رو نمیدونم ولی در مورد نمایشگاه میتونم راهنماییت کنم. جواب همه ی سوال ها رو هم بدون حرف اضافی بده. هیچ چیز اضافی نباشه و فقط جواب بده. {user_text}'''

    # ارسال به GPT
    response = requests.post(
        GPT_URL,
        headers={"Authorization": f"Bearer {GPT_API_KEY}"},
        json={
            "model": "gpt-4o",
            "messages": [{"role": "user", "content": prompt}]
        }
    )

    answer = response.json()["choices"][0]["message"]["content"]
    send_message(chat_id, answer)
    return "ok"

# اجرای Flask برای Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
