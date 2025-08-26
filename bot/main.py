# main.py
from pyrogram import Client, filters
import asyncio
from flask import Flask
import threading
import os

# ----------------------------
# Telegram Bot Initialization
# ----------------------------
bot = Client(
    "my_bot",
    api_id=int(os.environ.get("API_ID")),
    api_hash=os.environ.get("API_HASH"),
    bot_token=os.environ.get("BOT_TOKEN")
)

# Example handler (you can keep all your existing handlers)
@bot.on_message(filters.command("start"))
async def start_handler(client, message):
    await message.reply_text("🚀 AutoFilter Bot is running!")

# ----------------------------
# Web server for Koyeb health check
# ----------------------------
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!", 200

def run_webserver():
    # Koyeb requires 0.0.0.0 and port 8080
    app.run(host="0.0.0.0", port=8080)

# ----------------------------
# Start webserver in a separate thread
# ----------------------------
threading.Thread(target=run_webserver).start()

# ----------------------------
# Start Telegram bot
# ----------------------------
print("🚀 Telegram AutoFilter Bot starting...")
bot.run()
