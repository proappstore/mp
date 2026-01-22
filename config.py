import os
from dotenv import load_dotenv

load_dotenv()

# Provide your Bot token here or set BOT_TOKEN env var
BOT_TOKEN = os.getenv("BOT_TOKEN", "REPLACE_WITH_YOUR_TOKEN")

# Path to JSON DB
DB_PATH = os.getenv("DB_PATH", "data/db.json")