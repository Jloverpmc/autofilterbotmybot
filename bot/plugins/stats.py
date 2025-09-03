# bot/plugins/stats.py
from pyrogram import Client, filters
from pyrogram.types import Message
import bot.config as config
from bot.database.users import total_users
from bot.database.chats import total_chats
from bot.database.files import total_files

@Client.on_message(filters.command("stats") & filters.user(lambda uid: uid in config.ADMIN_IDS))
async def stats_cmd(bot: Client, message: Message):
    u = await total_users()
    c = await total_chats()
    f = await total_files()
    await message.reply(f"📊 Stats\nUsers: {u}\nChats: {c}\nFiles: {f}")
