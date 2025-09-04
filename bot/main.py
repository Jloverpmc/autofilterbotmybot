# bot/main.py
import asyncio
import logging
from pyrogram import Client
from fastapi import FastAPI
import uvicorn

# ---------------------------
# Logging (file + console)
# ---------------------------
logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
logging.getLogger().addHandler(console_handler)

# ---------------------------
# Import bot modules
# ---------------------------
try:
    import bot.config as config
    from bot.plugins import *
except Exception as e:
    logging.error(f"❌ Import error: {e}")

# ---------------------------
# Initialize Pyrogram client
# ---------------------------
app = Client(
    "autofilter-bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    plugins=dict(root="bot/plugins")
)

# ---------------------------
# Health check HTTP server for Koyeb
# ---------------------------
fastapi_app = FastAPI()

@fastapi_app.get("/")
async def health():
    return {"status": "ok"}

async def start_health_server():
    """Run FastAPI server in background"""
    config = uvicorn.Config(fastapi_app, host="0.0.0.0", port=8080, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

# ---------------------------
# Run both bot and health server
# ---------------------------
if __name__ == "__main__":
    async def main():
        logging.info("🚀 Starting Telegram AutoFilter Bot...")
        # Start health server in background
        asyncio.create_task(start_health_server())
        # Run Pyrogram bot
        await app.start()
        logging.info("✅ Bot started")
        # Keep bot running forever
        await asyncio.Event().wait()

    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f"❌ Bot crashed: {e}")
