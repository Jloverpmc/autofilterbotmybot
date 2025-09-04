import os
import uvicorn
from fastapi import FastAPI
from pyrogram import Client
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

# ----------------------------
# Vars from Environment
# ----------------------------
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URL = os.getenv("MONGO_URL")  # add in Koyeb vars

# ----------------------------
# Telegram Bot with Mongo storage
# ----------------------------
app_bot = Client(
    "my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    storage_uri=MONGO_URL  # <<< Use MongoDB for session
)

# ----------------------------
# FastAPI for healthcheck
# ----------------------------
app = FastAPI()

@app.get("/")
async def root():
    return {"status": "running"}

# ----------------------------
# Start bot & server
# ----------------------------
async def start_bot():
    await app_bot.start()
    print("🔹 Telegram Bot started...")

loop = asyncio.get_event_loop()
loop.create_task(start_bot())

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
