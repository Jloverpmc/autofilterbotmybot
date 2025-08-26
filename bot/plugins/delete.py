from bot.database.store import get_settings
from bot.utils.helpers import schedule_auto_delete, format_autodelete_time

async def send_file_with_autodelete(bot, chat_id: int, file_id: str, caption: str):
    s = await get_settings()
    secs = s.get("autodelete_seconds") or 0
    note = s.get("autodelete_note") or None
    expired = s.get("autodelete_expired") or None

    if secs and secs > 0:
        human = format_autodelete_time(secs)
        send_caption = (caption + "\n\n" if caption else "") + (note.format(autodelete_time=human) if note else "")
        m = await bot.send_document(chat_id, file_id, caption=send_caption)
        await schedule_auto_delete(bot, m.chat.id, m.id, secs, expired.format(autodelete_time=human) if expired else None)
        return m
    else:
        return await bot.send_document(chat_id, file_id, caption=caption)
        
