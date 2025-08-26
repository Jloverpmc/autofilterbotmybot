from bot.database.store import get_settings
from bot.utils.helpers import fill_caption
async def make_caption(meta: dict) -> str:
    s = await get_settings()
    tmpl = s.get('caption_template') or ''
    branding = s.get('branding') or ''
    meta = dict(meta or {})
    meta.setdefault('branding', branding)
    if not tmpl:
        return ''
    return fill_caption(tmpl, meta)
