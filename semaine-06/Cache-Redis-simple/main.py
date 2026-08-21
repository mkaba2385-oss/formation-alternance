import json
import os
import time
from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar

import redis
import requests


# Connexion à Redis
r = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True,
)


# Clé API OpenWeatherMap
API_KEY = os.environ["OPENWEATHER_API_KEY"]


# Typage générique du décorateur
P = ParamSpec("P")
T = TypeVar("T")


def make_cache_key(
    func_name: str,
    args: tuple[object, ...],
    kwargs: dict[str, object],
) -> str:
    """Crée une clé Redis unique."""
    return (
        f"cache:{func_name}:"
        f"{args}:"
        f"{tuple(sorted(kwargs.items()))}"
    )


def redis_cached(
    ttl: int = 300,
) -> Callable[
    [Callable[P, T]],
    Callable[P, T],
]:
    """Met en cache le résultat d'une fonction dans Redis."""

    def decorator(
        func: Callable[P, T],
    ) -> Callable[P, T]:
        @wraps(func)
        def wrapper(
            *args: P.args,
            **kwargs: P.kwargs,
        ) -> T:
            key = make_cache_key(
                func.__name__,
                args,
                kwargs,
            )

            # Vérifie si le résultat existe déjà
            cached = r.get(key)

            if cached is not None:
                print("Résultat trouvé dans Redis")
                return json.loads(cached)

            # Le résultat n'est pas dans Redis
            print("Résultat absent de Redis")

            # Appel de la vraie fonction
            result = func(*args, **kwargs)

            # Stockage dans Redis avec un TTL
            r.set(
                key,
                json.dumps(result),
                ex=ttl,
            )

            return result

        return wrapper

    return decorator


def invalidate_cache(
    func_name: str,
    args: tuple[object, ...],
    kwargs: dict[str, object],
) -> None:
    """Supprime une entrée précise du cache."""

    key = make_cache_key(
        func_name,
        args,
        kwargs,
    )

    r.delete(key)

    print("Cache supprimé")


@redis_cached(ttl=300)
def get_weather(city: str) -> dict[str, object]:
    """Récupère la météo actuelle d'une ville."""

    print(f"Appel de l'API pour {city}")

    response = requests.get(
        "https://api.openweathermap.org/data/2.5/weather",
        params={
            "q": city,
            "appid": API_KEY,
            "units": "metric",
            "lang": "fr",
        },
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    return {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"],
    }


def main() -> None:
    city = "Paris"

    print("--- Premier appel ---")

    start = time.perf_counter()

    weather = get_weather(city)

    duration = time.perf_counter() - start

    print(weather)
    print(f"Durée : {duration:.2f} secondes")

    print("\n--- Deuxième appel ---")

    start = time.perf_counter()

    weather = get_weather(city)

    duration = time.perf_counter() - start

    print(weather)
    print(f"Durée : {duration:.2f} secondes")

    print("\n--- Invalidation du cache ---")

    invalidate_cache(
        "get_weather",
        (city,),
        {},
    )

    print("\n--- Troisième appel après invalidation ---")

    start = time.perf_counter()

    weather = get_weather(city)

    duration = time.perf_counter() - start

    print(weather)
    print(f"Durée : {duration:.2f} secondes")


if __name__ == "__main__":
    main()