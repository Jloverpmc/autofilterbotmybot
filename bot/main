# main.py
import os
import asyncio
from fastapi import FastAPI
from pyrogram import Client

# =========================
# Environment / Config
# =========================
API_ID = int(os.environ.get("API_ID", 12345))
API_HASH = os.environ.get("API_HASH", "your_api_hash")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_bot_token")
PORT = int(os.environ.get("PORT", 8080))

# Pyrogram client
app_bot = Client(
    "autofilter_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="bot/plugins")
)

# FastAPI app
app = FastAPI(title="Telegram AutoFilter Bot")

# =========================
# Lifespan event handler
# =========================
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔹 Starting Telegram Bot...")
    await app_bot.start()
    yield
    print("🔹 Stopping Telegram Bot...")
    await app_bot.stop()

app.router.lifespan_context = lifespan

# =========================
# Simple health check route
# =========================
@app.get("/")
async def root():
    return {"status": "AutoFilter Bot is running!"}
