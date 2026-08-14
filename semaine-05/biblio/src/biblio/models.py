from datetime import date

from pydantic import BaseModel, Field


class Livre(BaseModel):
    id: int
    titre: str = Field(min_length=1)
    auteur: str = Field(min_length=1)
    annee: int = Field(ge=1000, le=2100)
    disponible: bool = True


class Emprunt(BaseModel):
    livre_id: int
    emprunteur: str = Field(min_length=1)
    date_emprunt: date
    date_retour_prevue: date
    date_retour_effective: date | None = None
