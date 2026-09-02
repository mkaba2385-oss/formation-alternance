from pathlib import Path
import pandas as pd

def lire_csv(chemin: str | Path, mois: str) -> pd.DataFrame:
    df = pd.read_csv(chemin)
    df["mois"] = mois
    return df

def charger_donnees(dossier: str | Path) -> pd.DataFrame:
    dossier = Path(dossier)
    fichiers = [
        ("janvier", dossier / "ventes_janvier.csv"),
        ("fevrier", dossier / "ventes_fevrier.csv"),
        ("mars", dossier / "ventes_mars.csv"),
        ("avril", dossier / "ventes_avril.csv"),
    ]
    frames = [lire_csv(path, mois) for mois, path in fichiers]
    return pd.concat(frames, ignore_index=True)

def agreger_ventes(df: pd.DataFrame) -> pd.DataFrame:
    rapport = df.groupby(["produit", "mois"], as_index=False)["ventes"].sum()
    ordre = ["janvier", "fevrier", "mars", "avril"]
    rapport["mois"] = pd.Categorical(rapport["mois"], categories=ordre, ordered=True)
    return rapport.sort_values(["produit", "mois"]).reset_index(drop=True)

def calculer_indicateurs(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["ventes_cumulees"] = df.groupby("produit")["ventes"].cumsum()
    df["croissance_mom_pct"] = (
        df.groupby("produit")["ventes"]
        .pct_change(fill_method=None)
        .mul(100)
        .round(2)
    )
    return df

def creer_rapport(dossier: str | Path, sortie: str | Path) -> pd.DataFrame:
    donnees = charger_donnees(dossier)
    rapport = calculer_indicateurs(agreger_ventes(donnees))
    rapport.to_csv(sortie, index=False, encoding="utf-8")
    return rapport
