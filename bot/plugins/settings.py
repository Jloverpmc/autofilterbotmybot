from pyrogram import Client, filters

@Client.on_message(filters.command('settings'))
async def settings(bot, message):
    await message.reply_text('Settings menu here.')
