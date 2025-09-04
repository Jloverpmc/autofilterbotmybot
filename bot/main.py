import os
import asyncio
from fastapi import FastAPI
from pyrogram import Client
from importlib import import_module
from pathlib import Path
from bot import config
import httpx

BOT_TOKEN = os.environ.get("BOT_TOKEN", config.BOT_TOKEN)
API_ID = int(os.environ.get("API_ID", config.API_ID))
API_HASH = os.environ.get("API_HASH", config.API_HASH)
PORT = int(os.environ.get("PORT", 8080))
KEEP_ALIVE_INTERVAL = 300  # seconds (5 minutes)

bot = Client(
    "autofilter",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH
)

# Automatically import all plugins
plugins_path = Path("bot/plugins")
for file in plugins_path.glob("*.py"):
    module_name = f"bot.plugins.{file.stem}"
    import_module(module_name)
    print(f"✅ Loaded plugin: {file.stem}")

async def keep_alive(url: str):
    async with httpx.AsyncClient() as client:
        while True:
            try:
                await client.get(url)
                print("🔄 Keep-alive ping sent")
            except Exception as e:
                print(f"⚠️ Keep-alive ping failed: {e}")
            await asyncio.sleep(KEEP_ALIVE_INTERVAL)

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting Telegram AutoFilter Bot...")
    await bot.start()
    print("✅ Bot started")

    # Start keep-alive task
    base_url = os.environ.get("BASE_URL", f"http://localhost:{PORT}")
    asyncio.create_task(keep_alive(base_url))

    yield
    print("🛑 Stopping Bot...")
    await bot.stop()
    print("✅ Bot stopped")

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
