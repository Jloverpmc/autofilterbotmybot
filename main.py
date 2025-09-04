import os
import asyncio
from fastapi import FastAPI
import uvicorn
from pyrogram import Client
import bot.config as config

# ---------------------------
# FastAPI app (for Koyeb healthcheck)
# ---------------------------
api = FastAPI()

@api.get("/")
async def root():
    return {"status": "ok", "message": "Bot is alive"}

# ---------------------------
# Pyrogram Client
# ---------------------------
bot = Client(
    "autofilter_bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    in_memory=True  # prevents sqlite session file issues
)

# ---------------------------
# Startup: Run both Bot + FastAPI
# ---------------------------
async def main():
    # Start Pyrogram bot
    await bot.start()
    print("✅ Bot started...")

    # Start FastAPI server
    config_port = int(os.environ.get("PORT", 8080))
    config_host = "0.0.0.0"

    server = uvicorn.Server(
        uvicorn.Config(api, host=config_host, port=config_port, log_level="info")
    )
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
