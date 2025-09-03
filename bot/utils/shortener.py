# bot/utils/shortener.py
import requests
from typing import Optional, Dict
import bot.config as config
from bot.database.store import get_global_settings

def _shorten_bitly(long_url: str, api_key: str) -> Optional[str]:
    try:
        r = requests.post(
            "https://api-ssl.bitly.com/v4/shorten",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={"long_url": long_url},
            timeout=10
        )
        if r.ok:
            return r.json().get("link")
    except Exception:
        return None
    return None

def _shorten_custom(long_url: str, api_url: str, api_key: str, extra: Dict) -> Optional[str]:
    try:
        params = {"url": long_url}
        if api_key: params["api_key"] = api_key
        params.update(extra or {})
        r = requests.get(api_url, params=params, timeout=10)
        if r.ok:
            try:
                j = r.json()
                for k in ("short","link","url"):
                    if k in j and isinstance(j[k], str):
                        return j[k]
            except Exception:
                if r.text.startswith("http"):
                    return r.text.strip()
    except Exception:
        pass
    return None

async def shorten_if_enabled(url: str) -> str:
    # synchronous helper is fine here; shortener config fetched from global settings if needed
    if not config.SHORT_ENABLED:
        return url
    # fallback to direct return for now
    return url
