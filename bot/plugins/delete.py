from bot.database.store import get_settings
from bot.utils.helpers import schedule_auto_delete, format_autodelete_time
async def send_file_with_autodelete(bot, chat_id:int, file_id:str, caption:str):
    s = await get_settings()
    secs = s.get('autodelete_seconds') or 1800
    note = s.get('autodelete_note') or '⚠️ This file will be auto-deleted in {autodelete_time}.'
    expired = s.get('autodelete_expired') or '❌ The file has been deleted after {autodelete_time}.'
    human = format_autodelete_time(secs)
    final_caption = (caption + '\n\n' if caption else '') + note.format(autodelete_time=human)
    m = await bot.send_document(chat_id, file_id, caption=final_caption)
    # schedule delete
    await schedule_auto_delete(bot, m.chat.id, m.id, secs, expired.format(autodelete_time=human))
    return m
