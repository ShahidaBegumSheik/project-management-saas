from time import time

from app.core.config import settings

_cache: dict[str, tuple[float, object]] = {}


def get_cached(key: str):
    item = _cache.get(key)
    if not item:
        return None
    expires_at, value = item
    if expires_at < time():
        _cache.pop(key, None)
        return None
    return value


def set_cached(key: str, value):
    _cache[key] = (time() + settings.cache_ttl_seconds, value)
    return value


def invalidate_prefix(prefix: str):
    for key in list(_cache.keys()):
        if key.startswith(prefix):
            _cache.pop(key, None)
