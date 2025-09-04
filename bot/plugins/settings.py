from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from bot.database.store import get_global_settings, update_global_setting
import json
import bot.config as config

# ---------------------------
# Keyboard
# ---------------------------
def settings_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📂 DB Channels", callback_data="settings:db")],
        [InlineKeyboardButton("📢 Dest Channels", callback_data="settings:dest")],
        [InlineKeyboardButton("🔔 Updates Channel", callback_data="settings:updates")],
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

# ---------------------------
# MongoDB-backed pending
# ---------------------------
# Structure: {_id: admin_id, key: key_waiting}
async def set_pending(admin_id: int, key: str):
    await update_global_setting(f"pending_{admin_id}", key)

async def get_pending(admin_id: int):
    gs = await get_global_settings()
    return gs.get(f"pending_{admin_id}")

async def clear_pending(admin_id: int):
    await update_global_setting(f"pending_{admin_id}", None)

# ---------------------------
# /settings command
# ---------------------------
@Client.on_message(filters.command("settings") & filters.private)
async def settings_cmd(bot: Client, message: Message):
    if message.from_user.id not in config.ADMIN_IDS:
        return await message.reply_text("❌ You are not allowed to use this command.")
    
    gs = await get_global_settings()
    text = "⚙️ **Current Settings:**\n"
    for k, v in gs.items():
        # skip internal pending keys
        if k.startswith("pending_"):
            continue
        text += f"• **{k}** = `{v}`\n"

    await message.reply_text(text, reply_markup=settings_kb())

# ---------------------------
# Callback buttons
# ---------------------------
@Client.on_callback_query(filters.regex(r"^settings:"))
async def settings_cb(bot, query):
    await query.answer()
    key = query.data.split(":", 1)[1]
    if key == "close":
        await query.message.delete()
        return

    prompts = {
        "db": "📂 Send DB channel IDs (comma separated).",
        "dest": "📢 Send destination channel IDs (comma separated).",
        "updates": "🔔 Send updates channel ID or @username.",
        "startmsg": "✨ Send Start Message (text/HTML).",
        "startpic": "🖼 Send Start Picture (photo or URL).",
        "forcesub": "🔒 Send Force Sub channel (@username or -100id). Blank = disable.",
        "forcemsg": "📑 Send Force Subscribe message.",
        "shortdet": "🔗 Send JSON: {\"provider\":\"...\",\"api_url\":\"...\",\"api_key\":\"...\"}",
        "shortmode": "⚡ Send `on` or `off`.",
        "caption": "📝 Send caption template. Variables: {filename} {size} {duration} {quality} {language} {subtitle} {episode} {season} {branding}",
        "branding": "🏷 Send branding/footer text.",
        "sticker": "🎭 Send sticker.",
        "autodelete": "🧹 Send auto-delete seconds (0 = disable).",
    }

    await query.message.reply_text(prompts.get(key, "Send value:"))
    await set_pending(query.from_user.id, key)

# ---------------------------
# Handle admin reply
# ---------------------------
@Client.on_message(filters.private & filters.user(lambda uid: uid in config.ADMIN_IDS))
async def settings_reply(bot: Client, message: Message):
    admin = message.from_user.id
    key = await get_pending(admin)
    if not key:
        return  # nothing waiting

    val = None
    try:
        if key == "startpic":
            val = message.photo.file_id if message.photo else message.text or message.caption
        elif key == "sticker":
            val = message.sticker.file_id if message.sticker else message.text
        elif key == "shortdet":
            val = json.loads(message.text)
        elif key == "autodelete":
            val = int(message.text.strip())
        elif key in ("db", "dest"):
            val = [x.strip() for x in (message.text or "").split(",") if x.strip()]
        elif key == "updates":
            val = message.text.strip()
        elif key == "shortmode":
            val = message.text.strip().lower() in ("on", "1", "true", "yes", "y")
        else:
            val = message.text or message.caption or ""
    except Exception as e:
        await message.reply(f"❌ Invalid input: {e}\nPlease try again.")
        return

    await update_global_setting(key, val)
    await clear_pending(admin)
    await message.reply(f"✅ Updated **{key}**.", reply_markup=settings_kb())
