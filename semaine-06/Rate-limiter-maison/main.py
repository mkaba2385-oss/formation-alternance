import redis

from rate_limiter import RateLimiter


redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True,
)


def main() -> None:
    redis_client.delete("user:1")

    limiter = RateLimiter(
        redis_client=redis_client,
        max_requests=3,
        window_seconds=60,
    )

    key = "user:1"

    for _ in range(5):
        allowed = limiter.is_allowed(key)

        if allowed:
            print("Autorisé : True")
        else:
            retry_after = limiter.get_retry_after(key)

            print(
                "Autorisé : False "
                f"- Réessayer dans {retry_after} secondes"
            )   
            