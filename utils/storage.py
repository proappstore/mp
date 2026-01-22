import json
import threading
import os
import config

_lock = threading.Lock()
DB_PATH = config.DB_PATH

def _ensure_db_file():
    d = os.path.dirname(DB_PATH)
    if d and not os.path.exists(d):
        os.makedirs(d, exist_ok=True)
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, "w") as f:
            json.dump({"users": {}, "orders": []}, f, indent=2)

def load_db():
    _ensure_db_file()
    with _lock:
        with open(DB_PATH, "r") as f:
            return json.load(f)

def save_db(db):
    _ensure_db_file()
    with _lock:
        with open(DB_PATH, "w") as f:
            json.dump(db, f, indent=2)

def ensure_user(uid, full_name=""):
    db = load_db()
    if uid not in db["users"]:
        db["users"][uid] = {"name": full_name, "upi": "", "wallet": 0, "orders": []}
        save_db(db)
    return db["users"][uid]