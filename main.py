from fastapi import FastAPI
from fastapi.responses import FileResponse
import uuid

app = FastAPI()

# Speicher
mailboxes = {}

# 📄 Seiten
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


# ✅ DAS HAT DIR GEFEHLT
@app.get("/send")
def send(to: str, msg: str):
    if to not in mailboxes:
        return {"status": "error", "message": "Email existiert nicht"}

    mailboxes[to].append(msg)
    return {"status": "ok"}