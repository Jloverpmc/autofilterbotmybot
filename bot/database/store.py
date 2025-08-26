from typing import Dict, Any
import bot.config as config

# try Motor (async Mongo) if MONGO_URI present
_db = None
try:
    if config.MONGO_URI:
        from motor.motor_asyncio import AsyncIOMotorClient
        _client = AsyncIOMotorClient(config.MONGO_URI)
        _db = _client[config.DB_NAME]
except Exception:
    _db = None

# in-memory fallback
_mem = {
    "settings": {
        "caption_template": None,
        "branding": config.BRANDING or "",
        "autodelete_seconds": None,
        "autodelete_note": None,
        "autodelete_expired": None,
        "force_sub": {"channel": config.FORCE_CHANNEL, "mode": config.FORCE_MODE},
        "shortener": {"enabled": config.SHORT_ENABLED, "provider": config.SHORT_PROVIDER, "api_url": config.SHORT_API_URL, "api_key": config.SHORT_API_KEY, "extra": {}},
        "dest_channels": [],
        "updates_channels": [],
        "db_channels": [],
        "start_text": None,
        "start_pic": None
    },
    "users": set()
}

async def get_settings() -> Dict[str, Any]:
    if _db:
        doc = await _db.settings.find_one({"_id":"global"}) or {}
        return doc.get("data", {})
    return _mem["settings"]

async def set_settings(data: Dict[str, Any]):
    if _db:
        await _db.settings.update_one({"_id":"global"},{"$set":{"data":data}}, upsert=True)
    else:
        _mem["settings"] = data

async def update_setting(k, v):
    s = await get_settings()
    s[k] = v
    await set_settings(s)

async def add_user(uid:int):
    if _db:
        await _db.users.update_one({"_id":uid},{"$set":{"_id":uid}}, upsert=True)
    else:
        _mem["users"].add(uid)

async def count_users() -> int:
    if _db:
        return await _db.users.count_documents({})
    return len(_mem["users"])
