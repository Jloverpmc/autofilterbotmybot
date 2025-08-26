import sys
import asyncio
from pyrogram import Client
import bot.config as config

def check_config():
    missing = []
    if not config.API_ID:
        missing.append("API_ID")
    if not config.API_HASH:
        missing.append("API_HASH")
    if not config.BOT_TOKEN:
        missing.append("BOT_TOKEN")
    if missing:
        print("[!] Missing config values:", ", ".join(missing))
        sys.exit(1)

check_config()

app = Client(
    "autofilter-bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    plugins=dict(root="bot/plugins")
)

async def main():
    await app.start()
    print("✅ Telegram AutoFilter Bot is connected!")
    
    # Optional: Keep Koyeb web server alive
    import aiohttp
    from aiohttp import web

    async def handle(request):
        return web.Response(text="✅ AutoFilter Bot is running!")

    web_app = web.Application()
    web_app.add_routes([web.get("/", handle)])
    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()
    print("🌐 Webserver running on port 8080")

    # Keep the bot running
    await asyncio.Event().wait()

if __name__ == "__main__":
    print("🚀 Starting AutoFilter Bot...")
    asyncio.run(main())
