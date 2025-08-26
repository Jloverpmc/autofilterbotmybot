import sys
from pyrogram import Client
import bot.config as config

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
        sys.exit(1)

check_config()

app = Client(
    "autofilter-bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    plugins=dict(root="bot/plugins")
)

if __name__ == "__main__":
    print("🚀 Telegram AutoFilter Bot starting...")
    app.run()
