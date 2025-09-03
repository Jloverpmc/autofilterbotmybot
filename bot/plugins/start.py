from pyrogram import Client, filters
from pyrogram.types import Message
from bot.database.store import get_global_settings

@Client.on_message(filters.command("start"))
async def start(bot: Client, message: Message):
    settings = await get_global_settings()
    start_msg = settings.get("startmsg") or "👋 Hello! I’m your AutoFilter Bot."
    start_pic = settings.get("startpic")

    if start_pic:
        await message.reply_photo(
            start_pic,
            caption=start_msg
        )
    else:
        await message.reply_text(start_msg)
