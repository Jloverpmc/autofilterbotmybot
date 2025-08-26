import bot.config as config
try:
    from bot.database.mongo import _db
except Exception:
    _db = None
mem = {
    'settings': {
        'caption_template': None,
        'branding': config.BRANDING or '',
        'autodelete_seconds': None,
        'autodelete_note': None,
        'autodelete_expired': None,
        'force_sub': {'channel': None, 'mode': None},
        'shortener': {'enabled': config.SHORT_ENABLED, 'provider': config.SHORT_PROVIDER, 'api_url': config.SHORT_API_URL, 'api_key': config.SHORT_API_KEY, 'extra': {}},
        'dest_channels': [], 'updates_channels': [], 'db_channels': [], 'start_text': None, 'start_pic': None
    },
    'users': set()
}
async def get_settings():
    if _db:
        doc = await _db.settings.find_one({'_id':'global'}) or {}
        return doc.get('data', {})
    return mem['settings']
async def set_settings(data):
    if _db:
        await _db.settings.update_one({'_id':'global'}, {'$set':{'data':data}}, upsert=True)
    else:
        mem['settings'] = data
async def update_setting(key, value):
    s = await get_settings()
    s[key] = value
    await set_settings(s)
async def add_user(uid):
    if _db:
        await _db.users.update_one({'_id':uid}, {'$set':{'_id':uid}}, upsert=True)
    else:
        mem['users'].add(uid)
async def count_users():
    if _db:
        return await _db.users.count_documents({})
    return len(mem['users'])
