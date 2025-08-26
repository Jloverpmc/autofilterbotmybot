from pyrogram import Client, filters
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.database.store import get_settings, update_setting

async def ensure_subscribed(bot, user_id: int):
    s = await get_settings()
    fs = s.get("force_sub") or {}
    channel = fs.get("channel")
    mode = fs.get("mode")
    if not channel or not mode:
        return True, None
    try:
        m = await bot.get_chat_member(channel, user_id)
        if mode == "join":
            ok = m.status in ("member","administrator","creator")
        else:
            ok = m.status in ("member","administrator","creator","restricted")
        if ok:
            return True, None
    except UserNotParticipant:
        pass
    btn = InlineKeyboardMarkup([[InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{str(channel).lstrip('@')}")]])
    return False, btn

# helper admin commands could be added (e.g., /forcesub) but settings UI is recommended.
