from pyrogram import Client
import bot.config as config, sys
def _check_config():
    miss = []
    if not getattr(config,'API_ID',None): miss.append('API_ID')
    if not getattr(config,'API_HASH',None): miss.append('API_HASH')
    if not getattr(config,'BOT_TOKEN',None): miss.append('BOT_TOKEN')
    if miss:
        print('[!] Missing in config.py: ' + ', '.join(miss))
        sys.exit(1)
_check_config()
app = Client('autofilter-bot', api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN, plugins=dict(root='bot/plugins'))
if __name__ == '__main__':
    print('Starting bot...')
    app.run()
