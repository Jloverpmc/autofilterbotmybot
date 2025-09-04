# bot/main.py

import logging
import asyncio
from pyrogram import Client

# ---------------------------
# Logging
# ---------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ---------------------------
# Imports
# ---------------------------
try:
    import bot.config as config
    from bot.plugins import *
    from bot.database import store, files
except Exception as e:
    logging.error(f"❌ Import error: {e}")

# ---------------------------
# Initialize Client
# ---------------------------
app = Client(
    "autofilter-bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    plugins=dict(root="bot/plugins")
)

# ---------------------------
# Bot Startup
# ---------------------------
async def start_bot():
    print("🚀 Telegram AutoFilter Bot starting...")

    # Initialize file counter in MongoDB
    await files.init_meta()

    # Start Pyrogram client
    await app.start()
    print("✅ Bot started")

    # Keep the bot running indefinitely
    stop_event = asyncio.Event()
    try:
        await stop_event.wait()
    finally:
        await app.stop()
        print("🛑 Bot stopped")

# ---------------------------
# Run
# ---------------------------
if __name__ == "__main__":
    try:
        asyncio.run(start_bot())
    except Exception as e:
        logging.error(f"❌ Bot crashed: {e}")
