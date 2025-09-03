# bot/plugins/post.py
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import bot.config as config
from bot.database.store import get_global_settings
from bot.utils.helpers import fill_caption
from bot.database.files import inc_files
from bot.plugins.caption import create_caption

# /post command for movies
@Client.on_message(filters.command("post") & filters.user(lambda uid: uid in config.ADMIN_IDS))
async def post_cmd(bot: Client, message: Message):
    """
    Usage:
    /post Title | 1080p-3.6GB:fid1,720p-1.4GB:fid2 | urls (optional comma separated)
    For simplicity this command expects quality:fileid pairs separated by commas
    Example:
    /post Movie Name | 1080p-3.6GB:AAABBB,720p-1.4GB:CCCFFF | https://link1,https://link2
    """
    text = message.text or ""
    try:
        _, payload = text.split(" ",1)
    except Exception:
        return await message.reply("❌ Usage: /post Title | q-size:fileid,q-size:fileid | urls")
    parts = [p.strip() for p in payload.split("|")]
    title = parts[0]
    qual_part = parts[1] if len(parts) > 1 else ""
    urls_part = parts[2] if len(parts) > 2 else ""

    qualities = []
    for it in qual_part.split(","):
        it = it.strip()
        if not it:
            continue
        if ":" in it:
            q_label, fid = it.split(":",1)
            if "-" in q_label:
                q, size = q_label.split("-",1)
            else:
                q, size = q_label, ""
            qualities.append({"quality": q.strip(), "size": size.strip(), "file_id": fid.strip()})
    urls = [u.strip() for u in urls_part.split(",") if u.strip()]

    # Build post text
    text_post = f"🎬 <b>{title}</b>\n\n🔊 Languages: Multiple\n\n🚀 Download Links ✨\n"
    for q in qualities:
        text_post += f"\n📦 {q['quality']} : {q['size']}\n"

    # show preview to admin with buttons: Dest channels list from settings
    gs = await get_global_settings()
    dests = gs.get("dest_channels") or []
    kb = []
    for ch in dests:
        kb.append([InlineKeyboardButton(f"Post → {ch}", callback_data=f"post_to:{ch}:{title}")])
    kb.append([InlineKeyboardButton("Cancel", callback_data="post_cancel")])
    await message.reply(text_post, reply_markup=InlineKeyboardMarkup(kb))

    # increment file counter
    await inc_files(len(qualities))
