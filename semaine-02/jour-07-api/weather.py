import requests

def get_temperature(lat : float, lon : float) -> float :
    """Retourne la température actuelle en degrés Celsius."""
    response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params= {
            "latitude": lat,
            "longitude": lon,
            "current_weather": True,
        },
        timeout = 5,
    )
    response.raise_for_status()
    data = response.json()
    return data["current_weather"]["temperature"]

if __name__ == "__main__" :
    # Coordonnées de Paris
    temp = get_temperature(48.85, 2.35)
    print(f"Il fait {temp}°C à Paris")
