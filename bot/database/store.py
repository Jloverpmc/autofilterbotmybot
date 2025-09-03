# bot/database/store.py
from motor.motor_asyncio import AsyncIOMotorClient
import bot.config as config
from typing import Dict, Any

_client = None
_db = None
if config.MONGO_URI:
    _client = AsyncIOMotorClient(config.MONGO_URI)
    _db = _client[config.DB_NAME]

# SETTINGS stored as single doc with _id = "global"
async def get_global_settings() -> Dict[str, Any]:
    if not _db:
        return {}
    doc = await _db.settings.find_one({"_id": "global"})
    return doc.get("data", {}) if doc else {}

async def set_global_settings(data: Dict[str, Any]):
    if not _db:
        return
    await _db.settings.update_one({"_id": "global"}, {"$set": {"data": data}}, upsert=True)

async def update_global_setting(key: str, value):
    s = await get_global_settings()
    s[key] = value
    await set_global_settings(s)

# Per-user settings (admins / storing preferences)
async def get_user_settings(user_id: int) -> Dict[str, Any]:
    if not _db:
        return {}
    doc = await _db.user_settings.find_one({"_id": user_id})
    return doc.get("data", {}) if doc else {}

async def set_user_settings(user_id: int, data: Dict[str, Any]):
    if not _db:
        return
    await _db.user_settings.update_one({"_id": user_id}, {"$set": {"data": data}}, upsert=True)

async def update_user_setting(user_id: int, key: str, value):
    s = await get_user_settings(user_id)
    s[key] = value
    await set_user_settings(user_id, s)
