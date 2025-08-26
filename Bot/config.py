import os
from dotenv import load_dotenv
load_dotenv()
API_ID = int(os.getenv('API_ID') or 0)
API_HASH = os.getenv('API_HASH') or ''
BOT_TOKEN = os.getenv('BOT_TOKEN') or ''
MONGO_URI = os.getenv('MONGO_URI') or ''   # mongodb+srv://...
DB_NAME = os.getenv('DB_NAME') or 'autofilter_bot'
ADMIN_IDS = set(int(x) for x in (os.getenv('ADMIN_IDS') or '').split() if x.isdigit())
BRANDING = os.getenv('BRANDING') or ''
DEFAULT_AUTODELETE_SECONDS = int(os.getenv('DEFAULT_AUTODELETE_SECONDS') or 1800)
DEFAULT_AUTODELETE_NOTE = os.getenv('DEFAULT_AUTODELETE_NOTE') or '⚠️ This file will be auto-deleted in {autodelete_time}.'
DEFAULT_AUTODELETE_EXPIRED = os.getenv('DEFAULT_AUTODELETE_EXPIRED') or '❌ The file has been deleted after {autodelete_time}.'
SHORT_ENABLED = os.getenv('SHORT_ENABLED','false').lower() in ('1','true','yes','on')
SHORT_PROVIDER = os.getenv('SHORT_PROVIDER') or 'custom'
SHORT_API_URL = os.getenv('SHORT_API_URL') or ''
SHORT_API_KEY = os.getenv('SHORT_API_KEY') or ''
