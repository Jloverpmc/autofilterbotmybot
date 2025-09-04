import os
import logging
from pyrogram import Client, filters
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI
import uvicorn

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URL = os.getenv("MONGO_URL")  # ✅ Now reads from MONGO_URL

# Telegram Bot client
app = Client(
    "autofilterbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# MongoDB connection
mongo_client = AsyncIOMotorClient(MONGO_URL)  # ✅ Use Koyeb Mongo URL
db = mongo_client["autofilterdb"]  # you can rename if needed

# FastAPI for health checks
web = FastAPI()

@web.get("/")
async def root():
    return {"status": "ok", "message": "Bot is running on Koyeb"}

# Example command
@app.on_message(filters.command("start"))
async def start_cmd(client, message):
    await message.reply_text("✅ Bot is alive and connected to MongoDB!")

if __name__ == "__main__":
    import asyncio

    async def start_all():
        await app.start()
        logger.info("🔹 Telegram Bot started successfully!")
        config = uvicorn.Config(web, host="0.0.0.0", port=8080, log_level="info")
        server = uvicorn.Server(config)
        await server.serve()

    asyncio.run(start_all())
