import os
import asyncio
from fastapi import FastAPI
from pyrogram import Client

# =========================
# FastAPI app
# =========================
app = FastAPI()

@app.get("/")
async def root():
    return {"status": "Bot is running!"}

# =========================
# Pyrogram Bot Client
# =========================
bot = Client(
    ":memory:",   # 👈 memory-only session (no sqlite file)
    api_id=int(os.environ.get("API_ID")),
    api_hash=os.environ.get("API_HASH"),
    bot_token=os.environ.get("BOT_TOKEN"),
    plugins=dict(root="bot/plugins")
)

# =========================
# Startup / Shutdown
# =========================
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(bot.start())
    print("🔹 Starting Telegram Bot...")

@app.on_event("shutdown")
async def shutdown_event():
    await bot.stop()
    print("🔹 Bot stopped.")

# =========================
# Run (Koyeb entrypoint)
# =========================
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port, workers=1, reload=False)
