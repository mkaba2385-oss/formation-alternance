from typing import Literal
from pydantic import BaseModel, Field, model_validator


class AlerteRequest(BaseModel):
    type_alerte: Literal["prix", "meteo", "diagnostic"]
    seuil: float | None = Field(default=None, description="Seuil numérique déclencheur")
    produit_code: str | None = Field(default=None, description="Code du produit pour l'alerte prix")
    region: str | None = Field(default=None, description="Région concernée par l'alerte")

    @model_validator(mode="after")
    def validate_cross_fields(self) -> "AlerteRequest":
        if self.type_alerte == "prix":
            if self.seuil is None or self.produit_code is None:
                raise ValueError("Pour une alerte de type 'prix', 'seuil' et 'produit_code' sont obligatoires.")

        elif self.type_alerte == "meteo":
            if self.region is None:
                raise ValueError("Pour une alerte de type 'meteo', 'region' est obligatoire.")

        elif self.type_alerte == "diagnostic":
            if self.seuil is not None or self.produit_code is not None or self.region is not None:
                raise ValueError("Pour une alerte de type 'diagnostic', aucun autre champ ('seuil', 'produit_code', 'region') ne doit être renseigné.")

        return self