import csv
from datetime import date
from typing import Literal
from pydantic import BaseModel, Field, ValidationError, field_validator
from .types import FcfaAmount, MaliPhone


MARCHES_VALIDES = {
    "Marché de Ségou",
    "Marché de Sikasso",
    "Marché de Mopti",
    "Marché de Bamako",
    "Marché de Kayes",
}


class PrixImportRow(BaseModel):
    culture: str = Field(..., min_length=2, max_length=50)
    marche: str
    prix_moyen: FcfaAmount
    unite: Literal["kg", "sac", "tonne", "panier"]
    date_releve: date
    telephone_source: MaliPhone

    @field_validator("marche")
    @classmethod
    def validate_marche(cls, v: str) -> str:
        if v not in MARCHES_VALIDES:
            raise ValueError(f"Marché inconnu '{v}'. Marchés valides : {', '.join(sorted(MARCHES_VALIDES))}")
        return v

    @field_validator("date_releve")
    @classmethod
    def validate_date_not_future(cls, v: date) -> date:
        if v > date.today():
            raise ValueError("La date de relevé ne peut pas être dans le futur.")
        return v


class RowError(BaseModel):
    ligne: int
    donnees: dict[str, str]
    erreurs: list[str]


class ImportResult(BaseModel):
    total_traite: int
    succes_count: int
    echec_count: int
    lignes_valides: list[PrixImportRow]
    erreurs: list[RowError]


def import_csv(path: str) -> ImportResult:
    lignes_valides: list[PrixImportRow] = []
    erreurs: list[RowError] = []
    total_lignes = 0

    with open(path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        
        for index, row in enumerate(reader, start=2):
            total_lignes += 1
            try:
                # Nettoyage basique des espaces sur chaque valeur du CSV
                cleaned_row = {k.strip(): v.strip() for k, v in row.items() if k}
                validated_row = PrixImportRow.model_validate(cleaned_row)
                lignes_valides.append(validated_row)

            except ValidationError as err:
                details_erreurs = [
                    f"{e['loc'][0]}: {e['msg']}" if e['loc'] else e['msg']
                    for e in err.errors()
                ]
                erreurs.append(
                    RowError(
                        ligne=index,
                        donnees=row,
                        erreurs=details_erreurs
                    )
                )

    return ImportResult(
        total_traite=total_lignes,
        succes_count=len(lignes_valides),
        echec_count=len(erreurs),
        lignes_valides=lignes_valides,
        erreurs=erreurs
    )


def afficher_rapport_import(result: ImportResult) -> None:
    print("RAPPORT D'IMPORTATION CSV")
    print(f"Total des lignes traitées : {result.total_traite}")
    print(f"Lignes importées avec succès : {result.succes_count}")
    print(f"Lignes rejetées : {result.echec_count}")

    if result.erreurs:
        print("\nDÉTAIL DES ERREURS :")
        for err in result.erreurs:
            print(f"\n[Ligne {err.ligne}]")
            print(f"  Données : {err.donnees}")
            print("  Raisons :")
            for msg in err.erreurs:
                print(f"   - {msg}")