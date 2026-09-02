import pandas as pd
from src.pipeline import lire_csv, charger_donnees, agreger_ventes, calculer_indicateurs, creer_rapport

def test_lire_csv_ajoute_le_mois(tmp_path):
    f = tmp_path / "ventes.csv"
    pd.DataFrame({"produit":["Souris"],"quantite":[10],"prix_unitaire":[25],"ventes":[250]}).to_csv(f,index=False)
    df = lire_csv(f, "janvier")
    assert df["mois"].iloc[0] == "janvier"

def test_charger_donnees_combine_les_csv():
    df = charger_donnees("data")
    assert len(df) == 16
    assert df["mois"].nunique() == 4

def test_agreger_ventes():
    df = pd.DataFrame({"produit":["Souris","Souris"],"mois":["janvier","janvier"],"ventes":[100,150]})
    result = agreger_ventes(df)
    assert len(result) == 1
    assert result.loc[0,"ventes"] == 250

def test_ventes_cumulees():
    df = pd.DataFrame({"produit":["Souris","Souris"],"mois":["janvier","fevrier"],"ventes":[100,150]})
    result = calculer_indicateurs(df)
    assert result["ventes_cumulees"].tolist() == [100,250]

def test_croissance_mom():
    df = pd.DataFrame({"produit":["Souris","Souris"],"mois":["janvier","fevrier"],"ventes":[100,120]})
    result = calculer_indicateurs(df)
    assert pd.isna(result["croissance_mom_pct"].iloc[0])
    assert result["croissance_mom_pct"].iloc[1] == 20.0
