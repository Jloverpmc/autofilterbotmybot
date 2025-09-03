# bot/plugins/autodelete.py
from pyrogram import Client, filters
from bot.database.store import get_global_settings
from bot.utils.helpers import schedule_auto_delete, format_autodelete_time

# This plugin reacts to messages sent by bot in DMs and schedules deletion if set.
# Actual scheduling performed by schedule_auto_delete called where files are sent.
# Left as placeholder for any centralized behavior if needed.
