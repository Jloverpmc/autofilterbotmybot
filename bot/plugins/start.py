from pyrogram import Client, filters

@Client.on_message(filters.command('start'))
async def start(bot, message):
    await message.reply_text('Hello! I am alive.')
