# bot/plugins/series_post.py
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import bot.config as config
from bot.database.files import inc_files

@Client.on_message(filters.command("sepseries") & filters.user(lambda uid: uid in config.ADMIN_IDS))
async def sepseries_cmd(bot: Client, message: Message):
    """
    Usage:
    /sepseries Series Name | S:1 | count:8 | 480p-200MB:fileid_template,720p-500MB:fileid_template | https://host/{ep}.mkv
    fileid_template may include {ep} to be replaced.
    Example:
    /sepseries Money Heist | S:1 | 8 | 480p-200MB:fid_{ep},720p-500MB:fid2_{ep} | https://host/mh_s1_e{ep}.mkv
    """
    text = message.text or ""
    try:
        _, payload = text.split(" ",1)
    except Exception:
        return await message.reply("❌ Usage: /sepseries Series | S:1 | count:8 | qualities | base_urls")
    segs = [s.strip() for s in payload.split("|")]
    series = segs[0]
    season = 1
    count = 1
    qualities = []
    base_url = segs[4] if len(segs) > 4 else ""
    for s in segs[1:]:
        if s.startswith("S:"):
            season = int(s.replace("S:","").strip())
        elif s.startswith("count:"):
            count = int(s.replace("count:","").strip())
        elif "-" in s and ":" in s:
            # e.g. 480p-200MB:fid_{ep}
            qpart, fidtmpl = s.split(":",1)
            quality,label = qpart.split("-",1)
            qualities.append({"quality": quality.strip(), "size": label.strip(), "fileid_template": fidtmpl.strip()})

    sent = []
    for ep in range(1, count+1):
        title = f"{series} S{season:02d}E{ep:02d}"
        text_post = f"📺 <b>{series}</b>\n🟢 Season {season} • Episode {ep}\n\nAvailable in:\n"
        kb = []
        for q in qualities:
            fid = q["fileid_template"].replace("{ep}", str(ep))
            label = f"{q['quality']} - {q['size']}"
            kb.append([InlineKeyboardButton(label, callback_data=f"dl:{fid}:{q['quality']}")])
            text_post += f"\n{label}"
        if base_url:
            link = base_url.replace("{ep}", str(ep))
            kb.append([InlineKeyboardButton("Link", url=link)])
        # post preview for admin (or directly post to updates/dest, depending on your workflow)
        msg = await message.reply(text_post, reply_markup=InlineKeyboardMarkup(kb))
        sent.append(msg)
        await inc_files(len(qualities))
    await message.reply(f"✅ {len(sent)} posts created (preview messages).")
