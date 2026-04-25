from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
import uuid
import os
import requests

app = FastAPI()

# 🧠 Speicher für Temp-Mail
mailboxes = {}

# 🔗 Discord Webhook
DISCORD_WEBHOOK = "DEIN_WEBHOOK_HIER"


# 📄 Frontend Seiten
@app.get("/")
def index():
    return FileResponse("templates/index.html")

@app.get("/index3")
def index3():
    return FileResponse("templates/index3.html")


# ✉️ Mail generieren
@app.get("/generate")
def generate():
    email = f"{uuid.uuid4().hex[:6]}@temp.local"
    mailboxes[email] = []
    return {"email": email}


# 📥 Inbox abrufen
@app.get("/api/inbox")
def inbox(email: str):
    return {"messages": mailboxes.get(email, [])}


# 📤 Nachricht senden (Temp-Mail System)
@app.get("/send")
def send(to: str, msg: str):
    if to not in mailboxes:
        return {"status": "error", "message": "Email existiert nicht"}

    mailboxes[to].append(msg)
    return {"status": "ok"}


# 🐞 Discord Bug System (NEW)
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


# 🚀 Render Start
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
