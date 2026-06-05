import os
from flask import Flask, request
import httpx

app = Flask(__name__)

TOKEN = os.getenv("TOKEN")
GEMINI_KEY = os.getenv("GEMINI_KEY")

API = f"https://api.telegram.org/bot{TOKEN}"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_KEY}"

def send(cid, txt):
    try: httpx.get(f"{API}/sendMessage", params={"chat_id":cid,"text":txt}, timeout=30)
    except: pass

def chat(user_msg):
    try:
        r = httpx.post(
            GEMINI_URL,
            json={
                "contents": [{
                    "parts": [{"text": f"تو یک دستیار هوشمند فارسی هستی. کوتاه و مفید جواب بده.\n\nکاربر: {user_msg}"}]
                }]
            },
            timeout=60
        )
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return "❌ خطا در اتصال به هوش مصنوعی"

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        msg = data["message"]
        cid = msg["chat"]["id"]
        txt = msg.get("text","")
        
        if txt == "/start": send(cid, "🚀 سلام! من دستیار هوشمند تو هستم با مغز Gemini.\nهر چی دوست داری بپرس.")
        elif txt == "/help": send(cid, "هر سوالی داری بپرس. هوش مصنوعی جواب میده.")
        elif txt.startswith("/"): send(cid, "✅ دریافت شد.")
        else:
            reply = chat(txt)
            send(cid, reply)
    
    return "ok"

@app.route("/", methods=["GET"])
def health():
    return "OK"
