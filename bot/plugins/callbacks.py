# bot/plugins/callbacks.py
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery
from bot.utils.helpers import fill_caption
from bot.database.store import get_global_settings
import bot.config as conf

@Client.on_callback_query()
async def generic_cb(client: Client, query: CallbackQuery):
    # This file can act as an extension point for callback patterns used across plugins.
    # Here we handle generic download button clicks like "dl:quality:fileid"
    data = query.data or ""
    if data.startswith("dl:"):
        # Format: dl:<fileid>:<quality>:<fname>
        parts = data.split(":",3)
        # parts: ['dl', fileid, quality, fname(optional)]
        if len(parts) >= 2:
            fileid = parts[1]
            quality = parts[2] if len(parts) > 2 else ""
            await query.answer("Preparing file... check your DM", show_alert=False)
            try:
                await client.send_document(query.from_user.id, fileid, caption=f"Requested {quality}")
            except Exception:
                await query.answer("Can't send file — maybe user hasn't started the bot.", show_alert=True)
