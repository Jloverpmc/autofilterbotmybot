import os
import asyncio
from fastapi import FastAPI
from pyrogram import Client

# ----- FastAPI App -----
app = FastAPI()

# ----- Pyrogram Bot -----
BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH")

bot = Client("autofilter-bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

# ----- Startup Event -----
@app.on_event("startup")
async def startup_event():
    print("🚀 Starting Telegram AutoFilter Bot...")
    asyncio.create_task(bot.start())

# ----- Shutdown Event -----
@app.on_event("shutdown")
async def shutdown_event():
    await bot.stop()
    print("🛑 Bot stopped.")

# ----- Simple Health Check -----
@app.get("/")
async def root():
    return {"status": "Bot is running"}

# ----- Run Uvicorn -----
if __name__ == "__main__":
    import uvicorn
    PORT = int(os.environ.get("PORT", 8080))  # Use Koyeb port variable
    uvicorn.run("main:app", host="0.0.0.0", port=PORT)
