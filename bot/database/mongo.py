from motor.motor_asyncio import AsyncIOMotorClient
import bot.config as config
_client = None
_db = None
if config.MONGO_URI:
    _client = AsyncIOMotorClient(config.MONGO_URI)
    _db = _client[config.DB_NAME]
async def get_settings_collection():
    return _db.settings if _db else None
async def get_users_collection():
    return _db.users if _db else None
