# session/session_manager.py

import json
import os

SESSION_FILE = "session/user_session.json"

def save_session(id_token):
    os.makedirs("session", exist_ok=True)
    session_data = {
        "id_token": id_token
    }
    with open(SESSION_FILE, "w") as f:
        json.dump(session_data, f)

def load_session():
    if not os.path.exists(SESSION_FILE):
        return None
    with open(SESSION_FILE, "r") as f:
        return json.load(f)

def clear_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
