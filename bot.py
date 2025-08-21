from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from config import API_ID, API_HASH, BOT_TOKEN, DB_CHANNEL_ID, ADMIN_IDS, BOT_USERNAME
from utils import get_search_results, get_size

app = Client("autofilterbot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Commandless group search
@app.on_message(filters.group)
async def group_search(client: Client, message: Message):
    text = message.text.strip()
    if not text:
        return
    
    # Get matching files from DB channel
    files = await get_search_results(DB_CHANNEL_ID, text)
    if not files:
        await message.reply_text("❌ Movie not available in the database.")
        return
    
    buttons = [
        [InlineKeyboardButton(f"{file.file_name} | {get_size(file.file_size)} | {file.language}", callback_data=f"sendpm#{file.file_id}")]
        for file in files[:10]
    ]
    
    await message.reply_text(
        "🎬 Search Results:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# Send file to PM
@app.on_callback_query(filters.regex(r"^sendpm#"))
async def send_file_pm(client, query):
    file_id = query.data.split("#")[1]
    user_id = query.from_user.id
    
    # Fetch file from DB channel
    msg = await client.get_messages(DB_CHANNEL_ID, int(file_id))
    
    # Send file in PM without default buttons
    await client.send_document(
        user_id,
        document=msg.document.file_id,
        caption=msg.caption or ""
    )
    await query.answer("File sent in PM ✅", show_alert=True)

# Admin Custom Button Example
@app.on_message(filters.command("addbutton") & filters.user(ADMIN_IDS))
async def add_custom_button(client, message):
    # Usage: /addbutton <file_id> <Button Text> <URL or callback>
    parts = message.text.split(maxsplit=3)
    if len(parts) != 4:
        return await message.reply_text("Usage: /addbutton <file_id> <Button Text> <URL>")
    
    file_id, text, url = parts[1], parts[2], parts[3]
    await client.send_message(
        message.chat.id,
        f"Custom button added for file {file_id}",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text, url=url)]])
    )

app.run()
