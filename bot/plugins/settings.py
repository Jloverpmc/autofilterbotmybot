# bot/plugins/settings.py
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from bot.database.store import get_global_settings, update_global_setting, update_global_setting as update_setting
import json
import bot.config as config

def settings_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📂 DB Channels", callback_data="settings:db")],
        [InlineKeyboardButton("📢 Dest Channels", callback_data="settings:dest")],
        [InlineKeyboardButton("🔔 Updates Channels", callback_data="settings:updates")],
        [InlineKeyboardButton("✨ Start Msg", callback_data="settings:startmsg")],
        [InlineKeyboardButton("🖼 Start Pic", callback_data="settings:startpic")],
        [InlineKeyboardButton("🔒 Force Sub", callback_data="settings:forcesub")],
        [InlineKeyboardButton("📑 Force Msg", callback_data="settings:forcemsg")],
        [InlineKeyboardButton("🔗 Short Det", callback_data="settings:shortdet")],
        [InlineKeyboardButton("⚡ Short Mode", callback_data="settings:shortmode")],
        [InlineKeyboardButton("📝 Caption", callback_data="settings:caption")],
        [InlineKeyboardButton("🎯 Branding", callback_data="settings:branding")],
        [InlineKeyboardButton("🎭 Sticker", callback_data="settings:sticker")],
        [InlineKeyboardButton("🧹 Auto Delete", callback_data="settings:autodelete")],
        [InlineKeyboardButton("❌ Close", callback_data="settings:close")],
    ])

@Client.on_message(filters.command("settings") & filters.user(lambda uid: uid in config.ADMIN_IDS))
async def settings_cmd(bot: Client, message: Message):
    gs = await get_global_settings()
    await message.reply_text("⚙️ Please choose the setting you want to update:", reply_markup=settings_kb())

# We'll use a simple in-memory pending map to know what admin is replying to
_pending = {}  # admin_id -> key awaiting

@Client.on_callback_query(filters.regex(r"^settings:"))
async def settings_cb(bot, query):
    key = query.data.split(":",1)[1]
    if key == "close":
        await query.message.delete()
        return
    prompts = {
        "db": "📂 Send DB channel ids (comma separated).",
        "dest": "📢 Send destination channel ids (comma separated).",
        "updates": "🔔 Send updates channel id or link.",
        "startmsg": "✨ Send Start Message (text/html).",
        "startpic": "🖼 Send Start Picture now (photo or URL).",
        "forcesub": "🔒 Send Force Sub channel (username with @ or -100id). Leave blank to disable.",
        "forcemsg": "📑 Send Force Subscribe message.",
        "shortdet": "🔗 Send Shortener details as JSON: {\"provider\":\"custom\",\"api_url\":\"...\",\"api_key\":\"...\"}",
        "shortmode": "⚡ Send 'on' or 'off' to toggle short mode.",
        "caption": "📝 Send caption template. Use variables: {filename} {size} {duration} {quality} {language} {subtitle} {episode} {season} {branding}",
        "branding": "🏷 Send branding/footer text.",
        "sticker": "🎭 Send sticker now.",
        "autodelete": "🧹 Send auto-delete seconds (0 to disable).",
    }
    await query.message.edit(prompts.get(key, "Send value:"))
    _pending[query.from_user.id] = key
    await query.answer()

@Client.on_message(filters.private & filters.user(lambda uid: uid in config.ADMIN_IDS))
async def settings_reply(bot: Client, message: Message):
    admin = message.from_user.id
    if admin not in _pending:
        return
    key = _pending.pop(admin)
    val = None

    # media handling
    if key == "startpic":
        if message.photo:
            val = message.photo.file_id
        else:
            val = message.text or message.caption
    elif key == "sticker":
        if message.sticker:
            val = message.sticker.file_id
        else:
            val = message.text
    elif key == "shortdet":
        # expect json
        try:
            val = json.loads(message.text)
        except Exception:
            await message.reply("❌ Invalid JSON. Send again.")
            _pending[admin] = key
            return
    elif key == "autodelete":
        try:
            val = int(message.text.strip())
        except Exception:
            await message.reply("❌ Invalid number. Send integer seconds.")
            _pending[admin] = key
            return
    elif key in ("db","dest","updates"):
        # comma separated list
        text = message.text or ""
        items = [x.strip() for x in text.split(",") if x.strip()]
        val = items
    elif key == "shortmode":
        val = (message.text.strip().lower() in ("on","1","true","yes","y"))
    else:
        val = message.text or message.caption or ""

    # update global settings in DB
    await update_setting(key, val)
    await message.reply(f"✅ Updated `{key}`.", reply_markup=settings_kb())
