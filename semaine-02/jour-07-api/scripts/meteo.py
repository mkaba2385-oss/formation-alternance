import os 
import sys 
import httpx

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city: str) -> None :
    if not API_KEY :
        print ("Erreur : La variable d'environnement OPENWEATHER_API_KEY est introuvable sur ton système.", file= sys.stderr)
        sys.exit(1)
    
    params = {
        "q" : city,
        "appid" : API_KEY,
        "units" : "metric",
        "lang" : "fr"
    }

    try :
        response = httpx.get(BASE_URL, params=params, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"]

        print(f"Météo pour {city} :")
        print(f" - Température : {temp}°C")
        print(f" - Humidité    : {humidity}%")
        print(f" - Climat      : {description}")

    except httpx.TimeoutException:
        print("Erreur : Temps d'attente dépassé (Timeout).", file=sys.stderr)
        sys.exit(1)
        
    except httpx.HTTPStatusError as e:
        status_code = e.response.status_code
        if status_code == 404:
            print(f"Erreur 404 : La ville '{city}' est introuvable", file=sys.stderr)

        elif status_code == 401:
            print("Erreur 401 : Clé API invalide ou non activée.", file=sys.stderr)
        else:
            print(f"Erreur HTTP {status_code} : {e.response.text}", file=sys.stderr)
            sys.exit(1)

    except httpx.RequestError as e:
        print(f"Erreur réseau : Impossible d'atteindre le serveur ({e})", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__" :
    if len(sys.argv) < 2:
        print("Usage : python3 scripts/meteo.py <nom_de_ville>")
        sys.exit(1)
    
    city_name = " ".join(sys.argv[1:])
    get_weather(city_name)
