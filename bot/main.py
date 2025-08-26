import asyncio
from pyrogram import Client
from aiohttp import web
import bot.config as config

# Config check
def check_config():
    miss = []
    if not config.API_ID:
        miss.append("API_ID")
    if not config.API_HASH:
        miss.append("API_HASH")
    if not config.BOT_TOKEN:
        miss.append("BOT_TOKEN")
    if miss:
        print("[!] Missing config values:", ", ".join(miss))
        exit(1)

check_config()

# Pyrogram Client
app = Client(
    "autofilter-bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    plugins=dict(root="bot/plugins")
)

# Fast web response
async def handle(request):
    return web.Response(text="✅ AutoFilter Bot is running!")

async def start_web():
    web_app = web.Application()
    web_app.add_routes([web.get("/", handle)])
    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()
    print("🌐 Webserver running on port 8080...")

async def main():
    await start_web()        # start web first
    await app.start()        # then start bot
    print("🚀 Telegram AutoFilter Bot started!")

    # Keep alive
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
