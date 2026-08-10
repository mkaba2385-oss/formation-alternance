from datetime import date, timedelta
from calcul_prix import RelevePrix, calculer_prix_moyen_30j


def test_calculer_prix_moyen_30j_succes():
    aujourdhui = date(2026, 8, 10)
    releves = [
        RelevePrix(produit="Maïs", prix=100.0, date_releve=aujourdhui - timedelta(days=5)),
        RelevePrix(produit="Maïs", prix=200.0, date_releve=aujourdhui - timedelta(days=15)),
        RelevePrix(produit="Maïs", prix=500.0, date_releve=aujourdhui - timedelta(days=40)), # Hors période (>30j)
        RelevePrix(produit="Riz", prix=300.0, date_releve=aujourdhui - timedelta(days=2)),    # Autre produit
    ]

    resultat = calculer_prix_moyen_30j(releves, produit="Maïs", date_reference=aujourdhui)

    assert resultat == 150.0