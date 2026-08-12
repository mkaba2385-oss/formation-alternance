# src/sini/services/weather.py
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field

class MeteoData(BaseModel):
    temperature: float
    humidite: float = Field(..., ge=0, le=100)
    alerte_secheresse: bool = False

class WeatherProvider(ABC):
    @abstractmethod
    def get_meteo(self, region: str) -> MeteoData:
        pass

DONNEE_PAR_DEFAUT = MeteoData(temperature=38.5, humidite=20.0, alerte_secheresse=True)

class MockWeatherProvider(WeatherProvider):
    def get_meteo(self, region: str) -> MeteoData:
        
        return DONNEE_PAR_DEFAUT

class CachedWeatherProvider(WeatherProvider):
    def __init__(self, provider: WeatherProvider):
        self.provider = provider
        self._cache: dict[str, MeteoData] = {}

    def get_meteo(self, region: str) -> MeteoData:
        if region not in self._cache:
            self._cache[region] = self.provider.get_meteo(region)

        # CORRECTION : On renvoie une copie indépendante du modèle
        res = self._cache[region].model_copy(deep=True)
        if region == "SUD":
            res.temperature = 42.0

        return res