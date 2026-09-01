import pandas as pd


df = pd.read_csv("titanic.csv")

df.info()

#

print(f"Nombre de valeurs manquantes par colonne : {df.isna().sum()}")

#

median_age = df["Age"].median()
df["Age"] = df["Age"].fillna(median_age)

#

threshold = 0.60

columns_to_drop = df.columns[df.isna().mean() > threshold]
df = df.drop(columns=columns_to_drop)

print(f"Colonnes supprimées : {columns_to_drop.to_list()}")

#

df["family_size"] = df["SibSp"] + df["Parch"]

#
df["title"] = df["Name"].str.extract(r",\s*([^.]*)\.")

#

df["title"] = df["title"].str.strip()

#

df.to_csv("titanic_clean.csv", index=False)

print(f"Dataset nettoyé sauvegardé dans titanic_clean.csv")