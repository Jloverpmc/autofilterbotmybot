# main.py
import asyncio
import os
from pyrogram import Client
from fastapi import FastAPI
import uvicorn

# --------------------------
# 🔹 Bot Configuration
# --------------------------
API_ID = int(os.environ.get("API_ID", 12345))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

bot = Client(
    "autofilter-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

# --------------------------
# 🔹 Load Plugins
# --------------------------
# Make sure all your plugins are inside bot/plugins/ as .py files
import glob
import importlib.util

plugins = glob.glob("bot/plugins/*.py")
for plugin in plugins:
    spec = importlib.util.spec_from_file_location(plugin, plugin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
print(f"✅ Loaded {len(plugins)} plugins.")

# --------------------------
# 🔹 FastAPI Web Server
# --------------------------
app = FastAPI()

@app.get("/")
async def home():
    return {"status": "Bot is alive!"}

# --------------------------
# 🔹 Run Bot + Web Server
# --------------------------
async def start_bot():
    async with bot:
        print("✅ Bot started")
        await asyncio.Future()  # keep running forever

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(start_bot())
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
