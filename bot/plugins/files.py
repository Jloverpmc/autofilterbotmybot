# bot/plugins/files.py
from pyrogram import Client, filters
from pyrogram.types import Message
from bot.plugins.caption import create_caption
from bot.database.store import get_global_settings
from bot.utils.helpers import schedule_auto_delete, format_autodelete_time

@Client.on_message((filters.document | filters.video | filters.audio) & filters.private)
async def handle_upload(client: Client, message: Message):
    # When admin or user sends file in DM to the bot: store or reply depending on role
    file_obj = message.document or message.video or message.audio
    # Prepare meta from message
    meta = {
        "filename": getattr(file_obj, "file_name", ""),
        "size": getattr(file_obj, "file_size", 0),
        "duration": getattr(file_obj, "duration", ""),
        "quality": "HD",
        "language": "",
        "subtitle": "",
    }
    caption = await create_caption(meta)
    # Send file back (echo) with caption (in real bot you'd store in DB or post)
    if message.document:
        m = await message.reply_document(message.document.file_id, caption=caption)
    elif message.video:
        m = await message.reply_video(message.video.file_id, caption=caption)
    else:
        m = await message.reply_document(file_obj.file_id, caption=caption)
    # Schedule auto delete if configured
    gs = await get_global_settings()
    secs = gs.get("autodelete_seconds") or config.DEFAULT_AUTODELETE_SECONDS
    if secs and secs > 0:
        human = format_autodelete_time(secs)
        note = gs.get("autodelete_note") or config.DEFAULT_AUTODELETE_NOTE
        expired = gs.get("autodelete_expired") or config.DEFAULT_AUTODELETE_EXPIRED
        # update caption with note (already sent above; optionally edit)
        # schedule deletion
        await schedule_auto_delete(client, m.chat.id, m.id, secs, expired.format(autodelete_time=human))
