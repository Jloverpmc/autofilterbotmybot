import os
import logging
from pyrogram import Client
from motor.motor_asyncio import AsyncIOMotorClient
from pyrogram import idle

# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Environment variables
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URL = os.getenv("MONGO_URL")  # from Koyeb env

# Initialize Telegram Bot
app_bot = Client(
    "autofilter-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="bot/plugins")  # auto-load plugins
)

# Initialize MongoDB
mongo_client = AsyncIOMotorClient(MONGO_URL)
db = mongo_client["autofilter_bot"]  # database name

# MongoDB test
async def check_mongo():
    try:
        await mongo_client.admin.command("ping")
        logger.info("✅ MongoDB Connected Successfully")
    except Exception as e:
        logger.error(f"❌ MongoDB Connection Failed: {e}")

# Main
if __name__ == "__main__":
    logger.info("🚀 Starting Telegram Bot...")
    app_bot.start()
    app_bot.loop.run_until_complete(check_mongo())
    idle()  # keep the bot running
    app_bot.stop()
