from motor.motor_asyncio import AsyncIOMotorClient
import bot.config as config

if not config.MONGO_URL:
    raise ValueError("MONGO_URL is not set!")

_db_client = AsyncIOMotorClient(config.MONGO_URL)
_db = _db_client[config.DB_NAME]  # e.g., "autofilter"

async def init_meta():
    """Ensure meta collection has the files counter initialized"""
    await _db.meta.update_one({"_id": "files"}, {"$setOnInsert": {"count": 0}}, upsert=True)

async def inc_files(n: int = 1):
    await _db.meta.update_one({"_id": "files"}, {"$inc": {"count": n}}, upsert=True)

async def total_files() -> int:
    doc = await _db.meta.find_one({"_id": "files"}) or {}
    return int(doc.get("count", 0))
