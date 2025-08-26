import asyncio
from aiohttp import web
from pyrogram import Client
import bot.config as config

# -----------------------------
# Create the Telegram bot client
# -----------------------------
app = Client(
    "autofilter-bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    plugins=dict(root="bot/plugins")
)

# -----------------------------
# Simple web server for Koyeb
# -----------------------------
async def handle(request):
    return web.Response(text="✅ AutoFilter Bot is running!")

async def start_bot(app_runner):
    await app.start()
    print("🚀 Telegram AutoFilter Bot started!")

async def stop_bot(app_runner):
    await app.stop()
    print("🛑 Telegram AutoFilter Bot stopped!")

# -----------------------------
# Main entry for Koyeb
# -----------------------------
if __name__ == "__main__":
    print("🌐 Webserver starting on port 8080...")

    # Create aiohttp app
    web_app = web.Application()
    web_app.add_routes([web.get('/', handle)])

    # Start Telegram bot in background
    loop = asyncio.get_event_loop()
    loop.create_task(start_bot(app))

    # Graceful shutdown
    web_app.on_cleanup.append(stop_bot)

    # Run web server on port 8080
    web.run_app(web_app, port=8080)
