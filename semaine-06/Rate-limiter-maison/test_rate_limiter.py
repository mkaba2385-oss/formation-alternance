import fakeredis
import time

from rate_limiter import RateLimiter


def test_exceed_limit() -> None:
    redis_client = fakeredis.FakeRedis()

    limiter = RateLimiter(
        redis_client=redis_client,
        max_requests=3,
        window_seconds=60,
    )

    assert limiter.is_allowed("user:1") is True
    assert limiter.is_allowed("user:1") is True
    assert limiter.is_allowed("user:1") is True

    assert limiter.is_allowed("user:1") is False


def test_multiple_keys_are_independent() -> None:
    redis_client = fakeredis.FakeRedis()

    limiter = RateLimiter(
        redis_client=redis_client,
        max_requests=2,
        window_seconds=60,
    )

    assert limiter.is_allowed("user:1") is True
    assert limiter.is_allowed("user:1") is True
    assert limiter.is_allowed("user:1") is False

    assert limiter.is_allowed("user:2") is True




def test_limit_resets_after_expiration() -> None:
    redis_client = fakeredis.FakeRedis()

    limiter = RateLimiter(
        redis_client=redis_client,
        max_requests=2,
        window_seconds=1,
    )

    assert limiter.is_allowed("user:1") is True
    assert limiter.is_allowed("user:1") is True
    assert limiter.is_allowed("user:1") is False

    time.sleep(1.1)

    assert limiter.is_allowed("user:1") is True

def test_retry_after() -> None:
    redis_client = fakeredis.FakeRedis()

    limiter = RateLimiter(
        redis_client=redis_client,
        max_requests=2,
        window_seconds=60,
    )

    key = "user:1"

    assert limiter.is_allowed(key) is True
    assert limiter.is_allowed(key) is True
    assert limiter.is_allowed(key) is False

    retry_after = limiter.get_retry_after(key)

    assert retry_after > 0
    assert retry_after <= 60