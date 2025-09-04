# bot/database/chats.py
import bot.config as config
try:
    from motor.motor_asyncio import AsyncIOMotorClient
    _db_client = AsyncIOMotorClient(config.MONGO_URL) if config.MONGO_URL else None
    _db = _db_client[config.DB_NAME] if _db_client else None
except Exception:
    _db = None

_mem_chats = set()

async def add_chat(cid: int):
    if _db:
        await _db.chats.update_one({"_id": cid}, {"$set": {"_id": cid}}, upsert=True)
    else:
        _mem_chats.add(cid)

async def total_chats() -> int:
    if _db:
        return await _db.chats.count_documents({})
    return len(_mem_chats)
