import motor.motor_asyncio
import os

MONGO_URL = os.environ["MONGO_URL"]
mongo_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)

db = mongo_client["autofilter"]
settings_col = db["settings"]

async def get_global_settings():
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
    await settings_col.update_one(
        {"_id": "global"},
        {"$set": {key: value}},
        upsert=True
    )

async def get_settings(chat_id: int):
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
    await settings_col.update_one(
        {"_id": str(chat_id)},
        {"$set": {key: value}},
        upsert=True
    )
