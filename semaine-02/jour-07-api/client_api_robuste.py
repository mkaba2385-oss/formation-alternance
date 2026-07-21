import requests
 
 
class WeatherClient:
    GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
    FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
    
    def __init__(self, timeout: int = 5):
        self.session = requests.Session()
        self.timeout = timeout
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
    
    def _geocode(self, city: str) -> tuple[float, float]:
        """Retourne (lat, lon) pour une ville."""
        r = self.session.get(
            self.GEOCODE_URL,
            params={"name": city, "count": 1},
            timeout=self.timeout,
        )
        r.raise_for_status()
        data = r.json()
        if "results" not in data or not data["results"]:
            raise ValueError(f"Ville introuvable : {city}")
        result = data["results"][0]
        return result["latitude"], result["longitude"]
    
    def get_current(self, city: str) -> dict:
        lat, lon = self._geocode(city)
        r = self.session.get(
            self.FORECAST_URL,
            params={
                "latitude": lat,
                "longitude": lon,
                "current_weather": True,
            },
            timeout=self.timeout,
        )
        r.raise_for_status()
        return r.json()["current_weather"]
    
    def get_forecast(self, city: str, days: int = 7) -> list[dict]:
        lat, lon = self._geocode(city)
        r = self.session.get(
            self.FORECAST_URL,
            params={
                "latitude": lat,
                "longitude": lon,
                "daily": "temperature_2m_max,temperature_2m_min",
                "timezone": "auto",
                "forecast_days": days,
            },
            timeout=self.timeout,
        )
        r.raise_for_status()
        daily = r.json()["daily"]
        return [
            {"date": d, "tmax": tmax, "tmin": tmin}
            for d, tmax, tmin in zip(
                daily["time"],
                daily["temperature_2m_max"],
                daily["temperature_2m_min"],
            )
        ]
 
 
if __name__ == "__main__":
    with WeatherClient() as client:
        current = client.get_current("Paris")
        print(f"Actuel à Paris : {current['temperature']}°C")
        
        forecast = client.get_forecast("Paris", days=5)
        for day in forecast:
            print(f"{day['date']} : {day['tmin']}°C à {day['tmax']}°C")
