import asyncio
from pyrogram import Client
import bot.config as config
from aiohttp import web

# Initialize Pyrogram client
app = Client(
    "autofilter-bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    plugins=dict(root="bot/plugins")
)

# Minimal web server for Koyeb health checks
async def handle(request):
    return web.Response(text="Bot is running ✅")

async def start_webserver():
    server = web.Application()
    server.router.add_get("/", handle)
    runner = web.AppRunner(server)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)  # Koyeb default port
    await site.start()
    print("🌐 Webserver running on port 8080")

# Start both bot and webserver
async def main():
    await asyncio.gather(app.start(), start_webserver())
    print("🚀 Telegram AutoFilter Bot started!")
    await app.idle()

if __name__ == "__main__":
    asyncio.run(main())
