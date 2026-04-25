from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
import uuid
import os
import json
import requests
import qrcode
from io import BytesIO
import base64

app = FastAPI()

# =========================
# 💾 DATABASE (JSON)
# =========================
DB_FILE = "load.json"

def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

mailboxes = load_db()

# =========================
# 🔗 DISCORD WEBHOOK
# =========================
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1497641585872212129/3ml7p4Kx9r6Nv0Sv-xVzqHE_Fh4jZbPdHuWziY5uTIanY8GOSLRSErXt32Ny5qielIho"


# =========================
# 📄 FRONTEND
# =========================
@app.get("/")
def index():
    return FileResponse("templates/index.html")

@app.get("/index3")
def index3():
    return FileResponse("templates/index3.html")


# =========================
# ✉️ GENERATE MAIL + QR
# =========================
@app.get("/generate")
def generate():
    email = f"{uuid.uuid4().hex[:6]}@temp.local"
    mailboxes[email] = []
    save_db(mailboxes)

    qr = qrcode.make(email)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")

    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    return {
        "email": email,
        "qr": qr_base64
    }


# =========================
# 📥 INBOX
# =========================
@app.get("/api/inbox")
def inbox(email: str):
    return {"messages": mailboxes.get(email, [])}


# =========================
# 📤 SEND MAIL
# =========================
@app.get("/send")
def send(to: str, msg: str):
    if to not in mailboxes:
        return {"status": "error", "message": "Email existiert nicht"}

    mailboxes[to].append(msg)
    save_db(mailboxes)

    return {"status": "ok"}


# =========================
# 🐞 DISCORD BUG SYSTEM
# =========================
@app.post("/bug/discord")
async def bug_discord(request: Request):
    data = await request.json()
    message = data.get("message", "No message")

    payload = {
        "content": f"🐞 **Bug Report**\n{message}"
    }

    try:
        requests.post(DISCORD_WEBHOOK, json=payload)
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "msg": str(e)}


# =========================
# 🚀 START (LOCAL + RENDER)
# =========================
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
