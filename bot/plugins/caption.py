# bot/plugins/caption.py
from bot.database.store import get_global_settings
from bot.utils.helpers import fill_caption

async def create_caption(meta: dict) -> str:
    gs = await get_global_settings()
    tmpl = gs.get("caption") or "{filename}"
    branding = gs.get("branding") or ""
    meta = dict(meta or {})
    meta.setdefault("branding", branding)
    return fill_caption(tmpl, meta)
