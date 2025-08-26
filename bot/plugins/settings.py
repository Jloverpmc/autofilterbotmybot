from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.database.store import get_settings, update_setting
import bot.config as config
import json

def settings_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📂 DB Channels", callback_data="settings:db")],
        [InlineKeyboardButton("📢 Dest Channels", callback_data="settings:dest")],
        [InlineKeyboardButton("🔔 Updates Channels", callback_data="settings:updates")],
        [InlineKeyboardButton("🚦 Force Subscribe", callback_data="settings:forcesub")],
        [InlineKeyboardButton("🏷️ Caption", callback_data="settings:caption")],
        [InlineKeyboardButton("✨ Branding", callback_data="settings:branding")],
        [InlineKeyboardButton("🔗 Short Det", callback_data="settings:shortdet")],
        [InlineKeyboardButton("🔗 Short Mode", callback_data="settings:shortmode")],
        [InlineKeyboardButton("🗑 Auto Delete", callback_data="settings:autodel")],
        [InlineKeyboardButton("❌ Close", callback_data="settings:close")],
    ])

@Client.on_message(filters.private & filters.command("settings") & filters.user(config.ADMIN_IDS))
async def settings_main(bot, message):
    await message.reply("⚙️ Please choose the setting you want to update:", reply_markup=settings_kb())

@Client.on_callback_query(filters.regex(r'^settings:'))
async def settings_router(bot, query):
    key = query.data.split(":",1)[1]
    s = await get_settings()
    if key == "root":
        return await query.message.edit("⚙️ Please choose the setting you want to update:", reply_markup=settings_kb())
    if key == "close":
        return await query.message.edit("Settings closed.")
    if key == "caption":
        current = s.get("caption_template") or "❌ Not set"
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("✍️ Set / Update", callback_data="caption:set")],
            [InlineKeyboardButton("🗑 Reset", callback_data="caption:reset")],
            [InlineKeyboardButton("⬅ Back", callback_data="settings:root")]
        ])
        text = ("📝 Caption Template\n\nUse variables:\n{filename} {size} {duration} {quality} {language} {subtitle} {episode} {season} {branding}\n\n"
                f"Current:\n<code>{current}</code>")
        return await query.message.edit(text, reply_markup=kb)
    if key == "branding":
        current = s.get("branding") or "❌ Not set"
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("✍️ Set / Update", callback_data="branding:set")],
            [InlineKeyboardButton("🗑 Reset", callback_data="branding:reset")],
            [InlineKeyboardButton("⬅ Back", callback_data="settings:root")]
        ])
        return await query.message.edit(f"✨ Branding\n\nCurrent:\n<code>{current}</code>", reply_markup=kb)
    if key == "autodel":
        secs = s.get("autodelete_seconds") or config.DEFAULT_AUTODELETE_SECONDS
        note = s.get("autodelete_note") or config.DEFAULT_AUTODELETE_NOTE
        expired = s.get("autodelete_expired") or config.DEFAULT_AUTODELETE_EXPIRED
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("⏱ Set Seconds", callback_data="autodel:setsecs")],
            [InlineKeyboardButton("✍️ Note (before)", callback_data="autodel:setnote")],
            [InlineKeyboardButton("✍️ Message (after)", callback_data="autodel:setexpired")],
            [InlineKeyboardButton("⬅ Back", callback_data="settings:root")]
        ])
        text = (f"🗑 Auto Delete Settings\n\nTime (seconds): <code>{secs}</code>\nBefore-note: <code>{note}</code>\nAfter-msg: <code>{expired}</code>")
        return await query.message.edit(text, reply_markup=kb)
    if key == "forcesub":
        fs = s.get("force_sub") or {}
        enabled = bool(fs and fs.get("channel"))
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ Set / Change Channel", callback_data="forcesub:set")],
            [InlineKeyboardButton("❌ Disable", callback_data="forcesub:disable")],
            [InlineKeyboardButton("⬅ Back", callback_data="settings:root")]
        ])
        current = f"Enabled: {fs.get('channel')} ({fs.get('mode')})" if enabled else "Disabled"
        return await query.message.edit(f"🚦 Force Subscribe\n\nCurrent: {current}", reply_markup=kb)
    if key == "shortdet":
        conf = s.get("shortener") or {}
        text = ("🔗 Shortener Details\n\n"
                f"Enabled: <code>{conf.get('enabled')}</code>\n"
                f"Provider: <code>{conf.get('provider')}</code>\n"
                f"API URL: <code>{conf.get('api_url') or '-'}</code>\n"
                f"API KEY: <code>{'****' if conf.get('api_key') else '-'}</code>\n"
                f"Extra JSON: <code>{json.dumps(conf.get('extra') or {}, ensure_ascii=False)}</code>")
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("✍️ Set Provider", callback_data="short:setprov")],
            [InlineKeyboardButton("✍️ Set API URL", callback_data="short:seturl")],
            [InlineKeyboardButton("✍️ Set API KEY", callback_data="short:setkey")],
            [InlineKeyboardButton("✍️ Set Extra JSON", callback_data="short:setextra")],
            [InlineKeyboardButton("⬅ Back", callback_data="settings:root")]
        ])
        return await query.message.edit(text, reply_markup=kb)
    if key == "shortmode":
        conf = s.get("shortener") or {}
        enabled = conf.get("enabled", False)
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔘 Toggle ON/OFF", callback_data="short:toggle")],
            [InlineKeyboardButton("⬅ Back", callback_data="settings:root")]
        ])
        return await query.message.edit(f"🔗 Short Mode is: <b>{'ON' if enabled else 'OFF'}</b>", reply_markup=kb)
    return await query.message.edit("🔧 Section not implemented yet.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="settings:root")]]))

# capture replies for set operations (simple implementation)
@Client.on_message(filters.private & filters.text & filters.user(lambda uid: uid in config.ADMIN_IDS))
async def capture_text(bot, message):
    if getattr(bot, "caption_wait", None) == message.from_user.id:
        await update_setting("caption_template", message.text)
        bot.caption_wait = None
        return await message.reply("✅ Caption template updated.")
    if getattr(bot, "branding_wait", None) == message.from_user.id:
        await update_setting("branding", message.text)
        bot.branding_wait = None
        return await message.reply("✅ Branding updated.")
    if getattr(bot, "autodel_secs_wait", None) == message.from_user.id:
        try:
            secs = int(message.text.strip())
        except:
            return await message.reply("❌ Invalid number.")
        await update_setting("autodelete_seconds", secs)
        bot.autodel_secs_wait = None
        return await message.reply(f"✅ Auto delete set to {secs} seconds.")
    # shortener fields handled similarly...
