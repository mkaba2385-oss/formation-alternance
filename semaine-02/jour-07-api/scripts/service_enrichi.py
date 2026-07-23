import argparse
import json
import os
import sys
import time
from pathlib import Path
import httpx

# --- CONFIGURATION ---
API_KEY = os.getenv("OPENWATCHER_API_KEY")
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
TIME_URL = "https://www.timeapi.io/api/v1/time/current/coordinate"
QUOTE_URL = "https://dummyjson.com/quotes/random"

CACHE_DIR = Path(".cache")
CACHE_TTL_SECONDS = 300  # 5 minutes


# --- FONCTIONS API ---

def get_weather(city: str) -> dict:
    if not API_KEY:
        return {
            "success": False,
            "message": "La variable d'environnement OPENWATCHER_API_KEY est introuvable"
        }

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "fr"
    }

    try:
        response = httpx.get(WEATHER_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        return {
            "success": True,
            "data": {
                "city": city,
                "country": data["sys"]["country"],
                "lat": data["coord"]["lat"],
                "lon": data["coord"]["lon"],
                "temp": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "description": data["weather"][0]["description"]
            }
        }

    except httpx.TimeoutException:
        return {
            "success": False,
            "error_type": "TIMEOUT",
            "message": "Le temps d'attente du serveur meteo est depasse"
        }

    except httpx.HTTPStatusError as e:
        status = e.response.status_code
        if status == 404:
            msg = f"La ville '{city}' est introuvable"
        elif status == 401:
            msg = "Cle API invalide"
        elif status >= 500:
            msg = f"Serveur meteo indisponible (code HTTP : {status})"
        else:
            msg = f"Erreur HTTP : {status}"

        return {
            "success": False,
            "error_type": "HTTP_Error",
            "code": status,
            "message": msg
        }

    except httpx.RequestError:
        return {
            "success": False,
            "error_type": "NETWORK_ERROR",
            "message": "Impossible d'atteindre l'API meteo (Reseau ou API Down)"
        }


def get_time(lat: float, lon: float) -> dict:
    params = {
        "latitude": lat,
        "longitude": lon
    }

    try:
        response = httpx.get(TIME_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        return {
            "success": True,
            "data": {
                "time": data.get("time"),
                "date": data.get("date"),
                "timeZone": data.get("timeZone")
            }
        }

    except httpx.TimeoutException:
        return {
            "success": False,
            "error_type": "TIMEOUT",
            "message": "Temps d'attente depasse pour l'API heure"
        }

    except httpx.HTTPStatusError as e:
        status = e.response.status_code
        return {
            "success": False,
            "error_type": "Error_Http",
            "code": status,
            "message": f"Erreur lors de la recuperation de l'heure : {status}"
        }

    except httpx.RequestError:
        return {
            "success": False,
            "error_type": "NETWORK_ERROR",
            "message": "Impossible de contacter l'API d'heure"
        }


def get_quote() -> dict:
    try:
        response = httpx.get(QUOTE_URL, timeout=5)
        response.raise_for_status()
        data = response.json()

        return {
            "success": True,
            "data": {
                "quote": data.get("quote"),
                "author": data.get("author")
            }
        }

    except httpx.TimeoutException:
        return {
            "success": False,
            "error_type": "TIMEOUT",
            "message": "Temps d'attente depasse pour l'API Dummyjson"
        }

    except httpx.HTTPStatusError as e:
        status = e.response.status_code
        return {
            "success": False,
            "error_type": "HTTP_ERROR",
            "code": status,
            "message": f"Erreur HTTP Dummyjson: {status}"
        }

    except httpx.RequestError:
        return {
            "success": False,
            "error_type": "NETWORK_ERROR",
            "message": "Impossible d'atteindre l'API Dummyjson "
        }


# --- GESTION DU CACHE DISQUE ---

def get_from_cache(city: str) -> dict | None:
    CACHE_DIR.mkdir(exist_ok=True)
    cache_file = CACHE_DIR / f"{city.lower().strip()}.json"

    if cache_file.exists():
        file_age = time.time() - cache_file.stat().st_mtime
        if file_age < CACHE_TTL_SECONDS:
            with open(cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
    return None


def save_to_cache(city: str, data: dict) -> None:
    CACHE_DIR.mkdir(exist_ok=True)
    cache_file = CACHE_DIR / f"{city.lower().strip()}.json"
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# --- ORGANISATION PRINCIPAL ---

def fetch_all(city: str) -> dict:
    cached_data = get_from_cache(city)
    if cached_data:
        cached_data["cached_response"] = True
        return cached_data

    weather_response = get_weather(city)

    if weather_response["success"]:
        lat = weather_response["data"]["lat"]
        lon = weather_response["data"]["lon"]
        time_response = get_time(lat, lon)
    else:
        time_response = {
            "success": False,
            "error_type": "DEPENDENCY_ERROR",
            "message": "Impossible d'obtenir l'heure sans les coordonnees meteo."
        }

    quote_response = get_quote()

    result = {
        "city": city,
        "cached_response": False,
        "weather": weather_response,
        "time": time_response,
        "quote": quote_response 
    }

    if weather_response["success"]:
        save_to_cache(city, result)

    return result


# --- INTERFACE EN LIGNE DE COMMANDE (CLI) ---

def main():
    parser = argparse.ArgumentParser(
        description="Affiche la meteo, l'heure locale et une citation pour une ville donnee."
    )
    parser.add_argument("city", type=str, help="Nom de la ville")
    parser.add_argument("--json", action="store_true", help="Formate la sortie en JSON")

    args = parser.parse_args()
    data = fetch_all(args.city)

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(f"\n=== Informations pour {args.city.capitalize()} ===")
        print(f"Source : {'Fichier de Cache' if data['cached_response'] else 'Appels API en direct'}\n")

        # 1. Météo
        if data["weather"]["success"]:
            w = data["weather"]["data"]
            print(f"[Meteo] : {w['temp']}°C, {w['description']} (Humidite: {w['humidity']}%)")
        else:
            print(f"[Erreur Meteo] : {data['weather']['message']}")

        # 2. Heure locale
        if data["time"]["success"]:
            t = data["time"]["data"]
            print(f"[Heure locale] : {t['time']} (Date: {t['date']}, Fuseau: {t['timeZone']})")
        else:
            print(f"[Erreur Heure] : {data['time']['message']}")

        # 3. Citation
        if data["quote"]["success"]:
            q = data["quote"]["data"]
            print(f"[Citation] : « {q['quote']} » - {q['author']}")
        else:
            print(f"[Erreur Citation] : {data['quote']['message']}")


if __name__ == "__main__":
    main()