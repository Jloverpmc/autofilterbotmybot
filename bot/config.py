# bot/config.py
import os
from dotenv import load_dotenv
load_dotenv()

def _to_bool(v):
    return str(v).lower() in ("1","true","yes","on","y")

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# MongoDB
MONGO_URL = os.getenv("MONGO_URL", "")  # e.g. mongodb+srv://user:pass@cluster/db
DB_NAME = os.getenv("DB_NAME", "mydatabase")

# Admins (space separated)
ADMIN_IDS = [int(x) for x in (os.getenv("ADMIN_IDS", "").split()) if x.isdigit()]

# Branding defaults
DEFAULT_BRANDING = os.getenv("BRANDING", "")

# Auto delete defaults (seconds)
DEFAULT_AUTODELETE_SECONDS = int(os.getenv("DEFAULT_AUTODELETE_SECONDS", "1800"))
DEFAULT_AUTODELETE_NOTE = os.getenv("DEFAULT_AUTODELETE_NOTE", "⚠️ This file will be auto-deleted in {autodelete_time}.")
DEFAULT_AUTODELETE_EXPIRED = os.getenv("DEFAULT_AUTODELETE_EXPIRED", "❌ The file has been deleted after {autodelete_time}.")

# Shortener placeholders
SHORT_ENABLED = _to_bool(os.getenv("SHORT_ENABLED","false"))
SHORT_PROVIDER = os.getenv("SHORT_PROVIDER","custom")  # bitly|custom
SHORT_API_URL = os.getenv("SHORT_API_URL","")
SHORT_API_KEY = os.getenv("SHORT_API_KEY","")

# Other
LOG_CHANNEL = os.getenv("LOG_CHANNEL", "")  # optional
