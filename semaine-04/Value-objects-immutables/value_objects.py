from dataclasses import dataclass, FrozenInstanceError
from math import radians, sin, cos, sqrt, atan2

# Money

@dataclass(frozen=True)
class Money:
    montant: float
    devise: str 
    def __post_init__(self):
        if self.montant < 0:
            raise ValueError("Le montant doit etre positif.")
        if not self.devise:
            raise ValueError("La devise est obligatoire.")

    def __add__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        if self.devise != other.devise:
            raise ValueError("Devises différentes.")
        return Money(self.montant + other.montant, self.devise)


# GpsPoint

@dataclass(frozen=True)
class GpsPoint:
    lat: float
    lon: float

    def __post_init__(self):
        if not (-90 <= self.lat <= 90):
            raise ValueError("Latitude invalide.")
        if not (-180 <= self.lon <= 180):
            raise ValueError("Longitude invalide.")

    def distance_to(self, other):
        R = 6371  # Rayon de la Terre en km
    
        lat1 = radians(self.lat)
        lon1 = radians(self.lon)
        lat2 = radians(other.lat)
        lon2 = radians(other.lon)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        return R * c

# PhoneNumber
@dataclass(frozen=True)
class PhoneNumber:
    numero: str
    pays: str

    def __post_init__(self):
        if not self.numero:
            raise ValueError("Numéro obligatoire.")
        if not self.pays:
            raise ValueError("Pays obligatoire.")