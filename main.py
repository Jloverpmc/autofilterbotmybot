# main.py
import os
import asyncio
from fastapi import FastAPI
from pyrogram import Client

# =========================
# Environment / Config
# =========================
API_ID = int(os.environ.get("API_ID", 12345))        # Replace with your API_ID
API_HASH = os.environ.get("API_HASH", "your_api_hash")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_bot_token")

# =========================
# Pyrogram Client
# =========================
# Using ":memory:" so no SQLite file is created (fixes "no such table: version" error)
app_bot = Client(
    ":memory:",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="bot/plugins")   # Folder containing your plugins
)

# =========================
# FastAPI App
# =========================
app = FastAPI(title="Telegram AutoFilter Bot")

# =========================
# Startup / Shutdown
# =========================
@app.on_event("startup")
async def startup_event():
    print("🔹 Starting Telegram Bot...")
    asyncio.create_task(app_bot.start())

@app.on_event("shutdown")
async def shutdown_event():
    print("🔹 Stopping Telegram Bot...")
    await app_bot.stop()

# =========================
# Health Check Route
# =========================
@app.get("/")
async def root():
    return {"status": "AutoFilter Bot is running!"}

# =========================
# Run directly (optional)
# =========================
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
