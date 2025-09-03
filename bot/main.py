# bot/main.py

import logging
from pyrogram import Client

# Enable logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

try:
    import bot.config as config
    from bot.plugins import *
    from bot.database import store
except Exception as e:
    logging.error(f"❌ Import error: {e}")

# Initialize client
app = Client(
    "autofilter-bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    plugins=dict(root="bot/plugins")
)

if __name__ == "__main__":
    try:
        print("🚀 Telegram AutoFilter Bot starting...")
        app.run()
    except Exception as e:
        logging.error(f"❌ Bot crashed: {e}")
