import asyncio
from typing import Dict
from bot.database.store import get_settings
from bot.config import DEFAULT_AUTODELETE_SECONDS, DEFAULT_AUTODELETE_NOTE, DEFAULT_AUTODELETE_EXPIRED

async def schedule_auto_delete(bot, chat_id: int, message_id: int, seconds: int, expired_text: str):
    try:
        await asyncio.sleep(seconds)
        await bot.delete_messages(chat_id, message_id)
        if expired_text:
            await bot.send_message(chat_id, expired_text)
    except Exception:
        pass

def format_autodelete_time(seconds: int) -> str:
    if seconds < 60:
        return f"{seconds} seconds"
    minutes = seconds // 60
    if minutes < 60:
        return f"{minutes} minutes"
    hours = minutes // 60
    if hours < 24:
        return f"{hours} hours"
    days = hours // 24
    return f"{days} days"

def fill_caption(template: str, meta: Dict[str, str]) -> str:
    if not template:
        return ""
    for key in ["filename","size","duration","quality","language","subtitle","episode","season","branding"]:
        template = template.replace("{"+key+"}", str(meta.get(key, "")))
    return template
    
