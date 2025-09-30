import json
from backend.config import AUTH_FILE

def load_auth():
    with open(AUTH_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_auth(data):
    with open(AUTH_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
