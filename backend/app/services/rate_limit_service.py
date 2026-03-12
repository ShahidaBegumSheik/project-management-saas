from collections import defaultdict, deque
from time import time

from fastapi import HTTPException, status

from app.core.config import settings

_attempts: dict[str, deque[float]] = defaultdict(deque)


def check_rate_limit(key: str):
    now = time()
    window = settings.login_rate_limit_window_seconds
    max_count = settings.login_rate_limit_count
    q = _attempts[key]
    while q and q[0] < now - window:
        q.popleft()
    if len(q) >= max_count:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many login attempts. Please try again later.",
        )
    q.append(now)


def reset_rate_limit(key: str):
    _attempts.pop(key, None)
