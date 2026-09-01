from pathlib import Path
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

MISSING_VALUES = ["", "NaN", "N/A", "null", "NULL", "None"]

def nettoyer_dataset(input_path: str | Path, output_path: str | Path) -> pd.DataFrame:
    logger.info("Lecture de %s", input_path)
    df = pd.read_csv(input_path, sep=";", na_values=MISSING_VALUES, keep_default_na=True)
    logger.info("Taille initiale : %s", df.shape)

    doublons = int(df.duplicated().sum())
    df = df.drop_duplicates().copy()
    logger.info("Doublons supprimés : %d", doublons)

    for col in ["nom", "ville", "statut", "email"]:
        df[col] = df[col].astype("string").str.strip()

    df["statut"] = (
        df["statut"].str.lower()
        .replace({"active": "actif", "inactive": "inactif"})
        .fillna("inconnu")
    )
    df["ville"] = df["ville"].fillna("inconnue")

    df["date_achat"] = pd.to_datetime(
        df["date_achat"], errors="coerce", format="mixed", dayfirst=True
    )
    df["age"] = pd.to_numeric(df["age"], errors="coerce")
    df["age"] = df["age"].fillna(df["age"].median())

    montant = df["montant"].astype("string").str.replace(" ", "", regex=False)
    montant = montant.str.replace(r"(?<=\d),(?=\d{3}\.)", "", regex=True)
    montant = montant.str.replace(",", ".", regex=False)
    df["montant"] = pd.to_numeric(montant, errors="coerce")

    avant = len(df)
    df = df.dropna(subset=["montant"]).copy()
    logger.info("Lignes sans montant supprimées : %d", avant - len(df))

    avant = len(df)
    df = df.dropna(subset=["date_achat"]).copy()
    logger.info("Lignes sans date supprimées : %d", avant - len(df))

    df["date_achat"] = df["date_achat"].dt.strftime("%Y-%m-%d")
    df.to_csv(output_path, sep=";", index=False, encoding="utf-8")

    logger.info("Fichier propre créé : %s", output_path)
    logger.info("Taille finale : %s", df.shape)
    return df

if __name__ == "__main__":
    nettoyer_dataset("dataset_sale.csv", "dataset_propre.csv")
