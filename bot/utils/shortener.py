import requests
from typing import Optional, Dict
from bot.database.store import get_settings
import bot.config as config

def _shorten_bitly(long_url: str, api_key: str) -> Optional[str]:
    try:
        r = requests.post("https://api-ssl.bitly.com/v4/shorten",
                          headers={"Authorization": f"Bearer {api_key}", "Content-Type":"application/json"},
                          json={"long_url": long_url}, timeout=10)
        if r.ok:
            return r.json().get("link")
    except Exception:
        return None
    return None

def _shorten_custom(long_url: str, api_url: str, api_key: str, extra: Dict) -> Optional[str]:
    params = {"url": long_url}
    if api_key: params["api_key"] = api_key
    if isinstance(extra, dict): params.update(extra)
    try:
        r = requests.get(api_url, params=params, timeout=10)
        if r.ok:
            try:
                j = r.json()
                # common keys
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
    s = await get_settings()
    conf = s.get("shortener") or {}
    enabled = conf.get("enabled", config.SHORT_ENABLED)
    if not enabled:
        return url
    provider = conf.get("provider", config.SHORT_PROVIDER)
    api_url = conf.get("api_url", config.SHORT_API_URL)
    api_key = conf.get("api_key", config.SHORT_API_KEY)
    extra = conf.get("extra", {})
    short = None
    if provider == "bitly":
        short = _shorten_bitly(url, api_key)
    else:
        short = _shorten_custom(url, api_url, api_key, extra)
    return short or url
  
