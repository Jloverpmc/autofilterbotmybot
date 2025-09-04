# main.py
import asyncio
import os
from pyrogram import Client
from fastapi import FastAPI

API_ID = int(os.environ.get("API_ID", 12345))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

bot = Client(
    "autofilter-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

# FastAPI app
app = FastAPI()

@app.get("/")
async def home():
    return {"status": "Bot is alive!"}

# Start bot when FastAPI starts
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(bot_start())

async def bot_start():
    async with bot:
        print("✅ Bot started")
        await asyncio.Future()  # keep running forever
