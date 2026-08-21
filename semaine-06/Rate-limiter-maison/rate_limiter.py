class RateLimiter:
    def __init__(
        self,
        redis_client,
        max_requests: int,
        window_seconds: int,
    ) -> None:
        self.redis_client = redis_client
        self.max_requests = max_requests
        self.window_seconds = window_seconds

    def is_allowed(self, key: str) -> bool:
        count = self.redis_client.incr(key)

        if count == 1:
            self.redis_client.expire(
                key,
                self.window_seconds,
            )

        return count <= self.max_requests

    def get_retry_after(self, key: str) -> int:
        return self.redis_client.ttl(key)