# bot/database/files.py
import bot.config as config
try:
    from motor.motor_asyncio import AsyncIOMotorClient
    _db_client = AsyncIOMotorClient(config.MONGO_URL) if config.MONGO_URL else None
    _db = _db_client[config.DB_NAME] if _db_client else None
except Exception:
    _db = None

_mem_count = 0

async def inc_files(n: int = 1):
    global _mem_count
    if _db:
        await _db.meta.update_one({"_id": "files"}, {"$inc": {"count": n}}, upsert=True)
    else:
        _mem_count += n

async def total_files() -> int:
    if _db:
        doc = await _db.meta.find_one({"_id": "files"}) or {}
        return int(doc.get("count", 0))
    return _mem_count
