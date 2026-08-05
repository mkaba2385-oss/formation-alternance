
import requests
import logging

class WeatherAlertService:
    def __init__(self, db_url: str, api_key: str):
        # Dépendances créées en dur (DIP violé)
        self.db_url = db_url
        self.api_key = api_key
        self.logger = logging.getLogger("Weather")

    def process_alerts(self, region: str):
        # 1. Fetch API
        resp = requests.get(f"https://api.weather.com/v1?region={region}&key={self.api_key}")
        data = resp.json()
        
        # 2. Filtrage & Analyse métier avec if/elif (OCP violé)
        alertes = []
        for hour in data["forecast"]:
            if hour["condition"] == "rain" and hour["pop"] > 0.7:
                alertes.append(f"Pluie forte prévue à {hour['time']}")
            elif hour["temp"] > 42:
                alertes.append("Alerte canicule : protégez les récoltes")
            elif hour["wind_speed"] > 60:
                alertes.append("Vents violents détectés")
                
        # 3. Sauvegarde en DB (SQL direct)
        # conn = connect(self.db_url)...
        
        # 4. Notification SMS direct via API externe
        for msg in alertes:
            requests.post("https://sms-provider.com/send", json={"msg": msg})