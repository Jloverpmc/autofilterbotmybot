# bot/database/store.py
from motor.motor_asyncio import AsyncIOMotorClient
import os

# Use MONGO_URI from environment only
MONGO_URI = os.environ["MONGO_URI"]

client = AsyncIOMotorClient(MONGO_URI)
db = client["autofilterbot"]

# Collections
settings_col = db["settings"]
global_col = db["global"]
files_col = db["files"]
posts_col = db["posts"]
series_col = db["series"]
users_col = db["users"]
channels_col = db["channels"]

# ---------------- GLOBAL SETTINGS ---------------- #
async def get_global_settings() -> dict:
    """Return global settings (single document)."""
    data = await global_col.find_one({"_id": "global"})
    if not data:
        data = {
            "_id": "global",
            "broadcast": True,
            "maintenance": False,
            "admins": []
        }
        await global_col.insert_one(data)
    return data

async def update_global_setting(key: str, value):
    await global_col.update_one(
        {"_id": "global"},
        {"$set": {key: value}},
        upsert=True
    )

# ---------------- CHAT SETTINGS ---------------- #
async def get_settings(chat_id: int) -> dict:
    data = await settings_col.find_one({"chat_id": chat_id})
    if not data:
        data = {
            "chat_id": chat_id,
            "caption": "",
            "branding": "",
            "force_sub": False,
            "force_msg": "",
            "short_mode": False,
            "short_det": "",
            "autodelete": False,
            "sticker": "",
            "start_pic": "",
            "start_msg": "",
            "db_channels": [],
            "dest_channels": [],
            "update_channels": []
        }
        await settings_col.insert_one(data)
    return data

async def update_setting(chat_id: int, key: str, value):
    await settings_col.update_one(
        {"chat_id": chat_id},
        {"$set": {key: value}},
        upsert=True
    )

# ---------------- FILES ---------------- #
async def add_file(file_id: str, name: str, size: int, caption: str = ""):
    await files_col.insert_one({
        "file_id": file_id,
        "name": name,
        "size": size,
        "caption": caption
    })

async def get_file(file_id: str):
    return await files_col.find_one({"file_id": file_id})

# ---------------- POSTS ---------------- #
async def add_post(post_id: int, chat_id: int, title: str, caption: str = ""):
    await posts_col.insert_one({
        "post_id": post_id,
        "chat_id": chat_id,
        "title": title,
        "caption": caption
    })

async def get_post(post_id: int):
    return await posts_col.find_one({"post_id": post_id})

# ---------------- SERIES ---------------- #
async def add_series(series_id: int, chat_id: int, title: str, episodes: list):
    await series_col.insert_one({
        "series_id": series_id,
        "chat_id": chat_id,
        "title": title,
        "episodes": episodes
    })

async def get_series(series_id: int):
    return await series_col.find_one({"series_id": series_id})

# ---------------- USERS ---------------- #
async def add_user(user_id: int, name: str = ""):
    await users_col.update_one(
        {"user_id": user_id},
        {"$set": {"name": name}},
        upsert=True
    )

async def get_user(user_id: int):
    return await users_col.find_one({"user_id": user_id})

# ---------------- CHANNELS ---------------- #
async def add_channel(chat_id: int, title: str, type_: str = "db"):
    """type_ = db / dest / update"""
    await channels_col.update_one(
        {"chat_id": chat_id},
        {"$set": {"title": title, "type": type_}},
        upsert=True
    )

async def get_channels(type_: str = None):
    if type_:
        return await channels_col.find({"type": type_}).to_list(None)
    return await channels_col.find().to_list(None)
