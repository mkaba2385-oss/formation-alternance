from dataclasses import dataclass
from datetime import date, timedelta
from typing import List


@dataclass
class RelevePrix:
    produit: str
    prix: float
    date_releve: date


def calculer_prix_moyen_30j(
    releves: List[RelevePrix], produit: str, date_reference: date
) -> float:
    limite = date_reference - timedelta(days=30)
    prix_valides = [
        p.prix
        for p in releves
        if p.produit == produit and limite <= p.date_releve <= date_reference
    ]

    if not prix_valides:
        return 0.0

    return sum(prix_valides) / len(prix_valides)