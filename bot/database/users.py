# bot/database/users.py
from typing import List
import bot.config as config
try:
    from motor.motor_asyncio import AsyncIOMotorClient
    _db_client = AsyncIOMotorClient(config.MONGO_URI) if config.MONGO_URI else None
    _db = _db_client[config.DB_NAME] if _db_client else None
except Exception:
    _db = None

_mem_users = set()

async def add_user(uid: int):
    if _db:
        await _db.users.update_one({"_id": uid}, {"$set": {"_id": uid}}, upsert=True)
    else:
        _mem_users.add(uid)

async def get_all_users() -> List[int]:
    if _db:
        cursor = _db.users.find({}, {"_id": 1})
        return [doc["_id"] async for doc in cursor]
    return list(_mem_users)

async def total_users() -> int:
    if _db:
        return await _db.users.count_documents({})
    return len(_mem_users)
