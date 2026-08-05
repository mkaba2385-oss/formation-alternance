from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Sequence

# -------------------------------------------------------------------
# 1. Domaine & Abstractions (DIP)
# -------------------------------------------------------------------

@dataclass(frozen=True)
class WeatherData:
    region: str
    temperature: float
    pop: float  # Probability of Precipitation
    wind_speed: float

@dataclass(frozen=True)
class Alert:
    region: str
    message: str
    severity: str

class WeatherProvider(ABC):
    @abstractmethod
    def fetch_weather(self, region: str) -> WeatherData:
        pass

class NotificationChannel(ABC):
    @abstractmethod
    def notify(self, alert: Alert) -> bool:
        pass

class AlertRepository(ABC):
    @abstractmethod
    def save(self, alert: Alert) -> None:
        pass

# -------------------------------------------------------------------
# 2. Alert Rules / Strategies (OCP)
# -------------------------------------------------------------------

class AlertRule(ABC):
    @abstractmethod
    def evaluate(self, weather: WeatherData) -> Alert | None:
        pass

class HeavyRainRule(AlertRule):
    def evaluate(self, weather: WeatherData) -> Alert | None:
        if weather.pop > 0.7:
            return Alert(
                region=weather.region,
                message="Pluie forte imminente. Préparez le drainage.",
                severity="HIGH"
            )
        return None

class HeatwaveRule(AlertRule):
    def evaluate(self, weather: WeatherData) -> Alert | None:
        if weather.temperature > 42.0:
            return Alert(
                region=weather.region,
                message="Alerte canicule : protégez les cultures sensibles.",
                severity="WARNING"
            )
        return None

class StrongWindRule(AlertRule):
    def evaluate(self, weather: WeatherData) -> Alert | None:
        if weather.wind_speed > 60.0:
            return Alert(
                region=weather.region,
                message="Vents violents prévus.",
                severity="MEDIUM"
            )
        return None

# -------------------------------------------------------------------
# 3. Orchestrateur (SRP & DIP)
# -------------------------------------------------------------------

class WeatherAlertService:
    """Orchestre le traitement des alertes sans connaître la techno sous-jacente."""

    def __init__(
        self,
        weather_provider: WeatherProvider,
        notifier: NotificationChannel,
        repository: AlertRepository,
        rules: Sequence[AlertRule],
    ):
        self.weather_provider = weather_provider
        self.notifier = notifier
        self.repository = repository
        self.rules = rules

    def process_region(self, region: str) -> list[Alert]:
        weather = self.weather_provider.fetch_weather(region)
        triggered_alerts: list[Alert] = []

        for rule in self.rules:
            alert = rule.evaluate(weather)
            if alert:
                self.repository.save(alert)
                self.notifier.notify(alert)
                triggered_alerts.append(alert)

        return triggered_alerts