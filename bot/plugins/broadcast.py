# bot/plugins/broadcast.py
from pyrogram import Client, filters
from pyrogram.types import Message
import bot.config as config
from bot.database.users import get_all_users

@Client.on_message(filters.command(["broadcast","bc"]) & filters.user(lambda uid: uid in config.ADMIN_IDS))
async def broadcast_cmd(bot: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply("Reply to a message to broadcast it.")
    users = await get_all_users()
    sent = failed = 0
    note = await message.reply("Broadcast starting...")
    for i, uid in enumerate(users, start=1):
        try:
            await message.reply_to_message.copy(uid)
            sent += 1
        except Exception:
            failed += 1
        if i % 50 == 0:
            try:
                await note.edit(f"Progress: {i}/{len(users)} (sent {sent}, failed {failed})")
            except:
                pass
    await note.edit(f"Broadcast finished. Sent: {sent}, Failed: {failed}")
