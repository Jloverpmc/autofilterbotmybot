from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.database.store import add_user, get_settings
from .force_subscribe import ensure_subscribed
@Client.on_message(filters.private & filters.command('start'))
async def start_cmd(bot, message):
    await add_user(message.from_user.id)
    ok, kb = await ensure_subscribed(bot, message.from_user.id)
    if not ok:
        return await message.reply('⚠️ Please join our channel to use the bot.', reply_markup=kb)
    s = await get_settings()
    text = s.get('start_text') or 'Hello {first_name}!'
    await message.reply(text.format(first_name=message.from_user.first_name))
