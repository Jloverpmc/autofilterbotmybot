# bot/database/store.py
import motor.motor_asyncio
import os

# ---------------------------
# 🔹 MongoDB Connection (from Koyeb env var)
# ---------------------------
MONGO_URL = os.environ["MONGO_URL"]  # must be set in Koyeb
mongo_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)

db = mongo_client["autofilter"]
settings_col = db["settings"]

# ---------------------------
# 🔹 GLOBAL SETTINGS
# ---------------------------
async def get_global_settings():
    """
    Return global settings (singleton doc with _id='global').
    Ensures the doc always exists.
    """
    doc = await settings_col.find_one({"_id": "global"})
    if not doc:
        doc = {
            "_id": "global",
            "startmsg": "👋 Hello! I’m your AutoFilter Bot.",
            "startpic": None,
            "caption": None,
        }
        await settings_col.insert_one(doc)
    return doc


async def update_global_setting(key: str, value):
    """
    Update one global setting key/value.
    Example: await update_global_setting("startmsg", "New welcome message")
    """
    await settings_col.update_one(
        {"_id": "global"},
        {"$set": {key: value}},
        upsert=True
    )

# ---------------------------
# 🔹 PER-CHAT SETTINGS (for groups/channels)
# ---------------------------
async def get_settings(chat_id: int):
    """
    Return settings for a specific chat.
    Ensures the doc always exists.
    """
    doc = await settings_col.find_one({"_id": str(chat_id)})
    if not doc:
        doc = {
            "_id": str(chat_id),
            "caption": None,
            "filters": {},
        }
        await settings_col.insert_one(doc)
    return doc


async def update_setting(chat_id: int, key: str, value):
    """
    Update a setting for a specific chat.
    Example: await update_setting(chat_id, "caption", "My custom caption")
    """
    await settings_col.update_one(
        {"_id": str(chat_id)},
        {"$set": {key: value}},
        upsert=True
    )
