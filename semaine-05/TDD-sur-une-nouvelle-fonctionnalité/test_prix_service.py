from datetime import date, timedelta
from sini.domain.prix import PrixProduit
from sini.services.prix_service import calculer_prix_moyen_30j


def test_calculer_prix_moyen_30j_succes():
    aujourdhui = date(2026, 8, 10)
    releves = [
        PrixProduit(produit="Maïs", prix=100.0, date_releve=aujourdhui - timedelta(days=5)),
        PrixProduit(produit="Maïs", prix=200.0, date_releve=aujourdhui - timedelta(days=15)),
        PrixProduit(produit="Maïs", prix=500.0, date_releve=aujourdhui - timedelta(days=40)), 
        PrixProduit(produit="Riz", prix=300.0, date_releve=aujourdhui - timedelta(days=2)),    
    ]

    resultat = calculer_prix_moyen_30j(releves, produit="Maïs", date_reference=aujourdhui)

    assert resultat == 150.0