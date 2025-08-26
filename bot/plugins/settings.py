from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.database.store import get_settings, update_setting
import bot.config as config, json
def kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton('📂 DB Channels', callback_data='settings:db')],
        [InlineKeyboardButton('📢 Dest Channels', callback_data='settings:dest')],
        [InlineKeyboardButton('🔔 Updates Channels', callback_data='settings:updates')],
        [InlineKeyboardButton('🚦 Force Subscribe', callback_data='settings:forcesub')],
        [InlineKeyboardButton('📝 Caption', callback_data='settings:caption')],
        [InlineKeyboardButton('✨ Branding', callback_data='settings:branding')],
        [InlineKeyboardButton('🔗 Short Det', callback_data='settings:shortdet')],
        [InlineKeyboardButton('🔗 Short Mode', callback_data='settings:shortmode')],
        [InlineKeyboardButton('🗑 Auto Delete', callback_data='settings:autodel')],
        [InlineKeyboardButton('❌ Close', callback_data='settings:close')],
    ])
@Client.on_message(filters.private & filters.command('settings') & filters.user(config.ADMIN_IDS))
async def settings_main(bot, message):
    await message.reply('⚙️ Choose setting:', reply_markup=kb())
@Client.on_callback_query(filters.regex(r'^settings:'))
async def router(bot, query):
    key = query.data.split(':',1)[1]
    s = await get_settings()
    if key == 'caption':
        current = s.get('caption_template') or 'Not set'
        return await query.message.edit('Caption current:\n<code>'+str(current)+'<code>', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('✍️ Set', callback_data='caption:set')],[InlineKeyboardButton('⬅ Back', callback_data='settings:root')]]))
    if key == 'forcesub':
        fs = s.get('force_sub') or {}
        enabled = bool(fs.get('channel'))
        kb2 = InlineKeyboardMarkup([[InlineKeyboardButton('➕ Set / Change', callback_data='forcesub:set')],[InlineKeyboardButton('❌ Disable', callback_data='forcesub:disable')],[InlineKeyboardButton('⬅ Back', callback_data='settings:root')]])
        text = 'Force Sub\nCurrent: ' + str(fs)
        return await query.message.edit(text, reply_markup=kb2)
    if key == 'shortdet':
        conf = s.get('shortener') or {}
        text = 'Shortener conf:\n' + str(conf)
        return await query.message.edit(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('✍️ Edit', callback_data='short:set')],[InlineKeyboardButton('⬅ Back', callback_data='settings:root')]]))
    return await query.message.edit('Section not ready', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('⬅ Back', callback_data='settings:root')]]))
