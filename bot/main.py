import logging
from pyrogram import Client
import asyncio

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

try:
    import bot.config as config
    from bot.plugins import *
    from bot.database import store, files
except Exception as e:
    logging.error(f"❌ Import error: {e}")

app = Client(
    "autofilter-bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    plugins=dict(root="bot/plugins")
)

async def start_bot():
    print("🚀 Telegram AutoFilter Bot starting...")
    await files.init_meta()  # Initialize file counter
    await app.start()
    print("✅ Bot started")
    await app.idle()
    await app.stop()
    print("🛑 Bot stopped")

if __name__ == "__main__":
    try:
        asyncio.run(start_bot())
    except Exception as e:
        logging.error(f"❌ Bot crashed: {e}")
