import re
from typing import Annotated
from pydantic import Field, AfterValidator


# 1. MaliPhone
def validate_mali_phone(v: str) -> str:
    cleaned = v.replace(" ", "")
    pattern = r"^(?:\+223)?[5-9]\d{7}$"
    if not re.match(pattern, cleaned):
        raise ValueError("Numéro de téléphone malien invalide. Exemple: +22370000000 ou 70000000")
    return cleaned

MaliPhone = Annotated[
    str,
    AfterValidator(validate_mali_phone),
    Field(examples=["+22370000000", "75123456"])
]


# 2. FcfaAmount 
FcfaAmount = Annotated[
    int,
    Field(ge=0, le=100_000_000, description="Montant en FCFA (0 à 100 000 000)", examples=[15000])
]


# 3. ParcelleName 
def validate_safe_name(v: str) -> str:
    pattern = r"^[a-zA-Z0-9\s\-_'’àâäéèêëîïôöùûüçÀÂÄÉÈÊËÎÏÔÖÙÛÜÇ]+$"
    if not re.match(pattern, v):
        raise ValueError("Le nom contient des caractères spéciaux non autorisés.")
    return v

ParcelleName = Annotated[
    str,
    Field(min_length=1, max_length=100, examples=["Champ Ségou Nord"]),
    AfterValidator(validate_safe_name)
]


# 4. GpsCoordinatesMali 
MALI_LAT_MIN, MALI_LAT_MAX = 10.0, 25.0
MALI_LON_MIN, MALI_LON_MAX = -12.5, 4.5

def validate_mali_gps(coords: tuple[float, float]) -> tuple[float, float]:
    lat, lon = coords
    if not (MALI_LAT_MIN <= lat <= MALI_LAT_MAX and MALI_LON_MIN <= lon <= MALI_LON_MAX):
        raise ValueError(
            f"Les coordonnées GPS ({lat}, {lon}) sont hors des limites du Mali "
            f"(Lat: [{MALI_LAT_MIN}, {MALI_LAT_MAX}], Lon: [{MALI_LON_MIN}, {MALI_LON_MAX}])."
        )
    return coords

GpsCoordinatesMali = Annotated[
    tuple[float, float],
    AfterValidator(validate_mali_gps),
    Field(description="Coordonnées GPS (latitude, longitude) au Mali", examples=[(12.6392, -8.0029)])
]