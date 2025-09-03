from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.database.store import get_settings

@Client.on_message(filters.command("start") & filters.private)
async def start(client, message):
    user_id = message.from_user.id
    settings = await get_settings()

    start_msg = settings.get("start_msg", "👋 Hello, I’m your AutoFilter Bot!")
    start_pic = settings.get("start_pic")

    buttons = [
        [InlineKeyboardButton("⚙️ Settings", callback_data="open_settings")],
        [InlineKeyboardButton("📢 Updates", url=settings.get("updates_channel", "https://t.me/YourUpdates"))],
    ]

    if start_pic:
        await message.reply_photo(
            photo=start_pic,
            caption=start_msg,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    else:
        await message.reply_text(
            start_msg,
            reply_markup=InlineKeyboardMarkup(buttons)
        )

# open /settings menu from inline button
@Client.on_callback_query(filters.regex("^open_settings$"))
async def open_settings(client, query):
    from bot.plugins.settings import settings_kb
    await query.message.edit("⚙️ **Bot Settings**", reply_markup=settings_kb())
