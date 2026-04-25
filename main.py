from fastapi import FastAPI
from fastapi.responses import FileResponse
import uuid
import os

app = FastAPI()

# Speicher für Temp-Mail
mailboxes = {}

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


# 📤 Nachricht senden
@app.get("/send")
def send(to: str, msg: str):
    if to not in mailboxes:
        return {"status": "error", "message": "Email existiert nicht"}

    mailboxes[to].append(msg)
    return {"status": "ok"}


# 🚀 Render / Production Start
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
