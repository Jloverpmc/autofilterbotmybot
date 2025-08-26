import os
from dotenv import load_dotenv
load_dotenv()

def _to_bool(v):
    if v is None: return False
    return str(v).strip().lower() in ("1","true","yes","on","y")

API_ID = int(os.getenv("API_ID","0"))
API_HASH = os.getenv("API_HASH","")
BOT_TOKEN = os.getenv("BOT_TOKEN","")

# MongoDB (optional)
MONGO_URI = os.getenv("MONGO_URI","")   # e.g. mongodb+srv://...
DB_NAME = os.getenv("DB_NAME","autofilter_bot")

# Admin IDs (space-separated)
ADMIN_IDS = {int(x) for x in os.getenv("ADMIN_IDS","").split() if x.strip().isdigit()}

# Bot basics
BOT_NAME = os.getenv("BOT_NAME","AutoFilterBot")
BRANDING = os.getenv("BRANDING","")   # will be inserted into captions as {branding}

# Force subscribe defaults (can be changed in settings)
FORCE_SUB_ENABLED = _to_bool(os.getenv("FORCE_SUB_ENABLED","false"))
FORCE_CHANNEL = os.getenv("FORCE_CHANNEL","")   # @channelusername or -100id
FORCE_MODE = os.getenv("FORCE_MODE","join")     # "join" or "request"
FORCE_MSG = os.getenv("FORCE_MSG","Please join the channel to use this bot.")

# Auto-delete defaults
DEFAULT_AUTODELETE_SECONDS = int(os.getenv("DEFAULT_AUTODELETE_SECONDS","1800"))
DEFAULT_AUTODELETE_NOTE = os.getenv("DEFAULT_AUTODELETE_NOTE","⚠️ This file will be auto-deleted in {autodelete_time}.")
DEFAULT_AUTODELETE_EXPIRED = os.getenv("DEFAULT_AUTODELETE_EXPIRED","❌ The file has been deleted after {autodelete_time}.")

# Shortener defaults
SHORT_ENABLED = _to_bool(os.getenv("SHORT_ENABLED","false"))
SHORT_PROVIDER = os.getenv("SHORT_PROVIDER","custom")  # bitly|custom|gplinks|droplink
SHORT_API_URL = os.getenv("SHORT_API_URL","")
SHORT_API_KEY = os.getenv("SHORT_API_KEY","")
