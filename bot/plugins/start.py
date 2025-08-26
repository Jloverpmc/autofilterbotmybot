from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.database.store import add_user, get_settings

@Client.on_message(filters.private & filters.command("start"))
async def start_cmd(bot, message):
    await add_user(message.from_user.id)
    s = await get_settings()
    start_text = s.get("start_text") or f"Hello {message.from_user.first_name} — welcome!"
    kb = InlineKeyboardMarkup([[InlineKeyboardButton("⚙ Settings", callback_data="settings:root")]])
    await message.reply(start_text, reply_markup=kb)
