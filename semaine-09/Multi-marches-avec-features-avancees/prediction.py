import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


np.random.seed(42)

marches = [
    "Segou",
    "Bamako",
    "Mopti",
    "Sikasso",
    "Tombouctou",
]

dates = pd.date_range(
    start="2025-01-01",
    periods=365,
    freq="D",
)

donnees = []

for marche in marches:

    prix_depart = np.random.uniform(220, 300)

    for i, date in enumerate(dates):

       
        tendance = i * 0.08

        saison = 10 * np.sin(
            2 * np.pi * i / 365
        )

        
        pluie = max(
            0,
            80 * np.sin(
                2 * np.pi * (i - 80) / 365
            ) + np.random.normal(0, 10),
        )

       
        change = (
            600
            + 20 * np.sin(2 * np.pi * i / 365)
            + np.random.normal(0, 5)
        )

       
        effet_marche = {
            "Segou": 0,
            "Bamako": 20,
            "Mopti": 10,
            "Sikasso": -5,
            "Tombouctou": 30,
        }[marche]

        bruit = np.random.normal(0, 8)

        prix = (
            prix_depart
            + tendance
            + saison
            + effet_marche
            - pluie * 0.03
            + change * 0.02
            + bruit
        )

        donnees.append({
            "date": date,
            "marche": marche,
            "prix": prix,
            "precipitations": pluie,
            "change": change,
            "mois": date.month,
        })


df = pd.DataFrame(donnees)

print("=== DATASET ===")
print(df.head())

print("\nDimensions :", df.shape)

print("\nMarchés :")
print(df["marche"].unique())

print("\nValeurs manquantes :")
print(df.isnull().sum())


for lag in [1, 2, 3, 7, 14]:

    df[f"lag_{lag}"] = (
        df.groupby("marche")["prix"]
        .shift(lag)
    )



df["moyenne_7"] = (
    df.groupby("marche")["prix"]
    .transform(
        lambda x: x.shift(1).rolling(7).mean()
    )
)


df["target_7j"] = (
    df.groupby("marche")["prix"]
    .shift(-7)
)


df = df.dropna().reset_index(drop=True)


print("\n=== DATASET FINAL ===")
print(df.head())


dates_uniques = sorted(
    df["date"].unique()
)

date_test = dates_uniques[-90]

train = df[
    df["date"] < date_test
].copy()

test = df[
    df["date"] >= date_test
].copy()

print("\n=== SPLIT ===")
print("Train :", train["date"].min(), "→", train["date"].max())
print("Test  :", test["date"].min(), "→", test["date"].max())


features = [
    "lag_1",
    "lag_2",
    "lag_3",
    "lag_7",
    "lag_14",
    "moyenne_7",
    "precipitations",
    "change",
    "mois",
]

target = "target_7j"


X_train = train[
    features + ["marche"]
]

y_train = train[target]

X_test = test[
    features + ["marche"]
]

y_test = test[target]


preprocessor_global = ColumnTransformer([
    (
        "num",
        StandardScaler(),
        features,
    ),
    (
        "cat",
        OneHotEncoder(
            handle_unknown="ignore"
        ),
        ["marche"],
    ),
])


modele_global = Pipeline([
    (
        "preprocessor",
        preprocessor_global,
    ),
    (
        "model",
        RandomForestRegressor(
            n_estimators=150,
            random_state=42,
            n_jobs=-1,
        ),
    ),
])


modele_global.fit(
    X_train,
    y_train,
)

pred_global = modele_global.predict(
    X_test
)


pred_par_marche = np.zeros(
    len(test)
)

modeles_marches = {}

for marche in marches:

    train_m = train[
        train["marche"] == marche
    ]

    test_m = test[
        test["marche"] == marche
    ]

    X_train_m = train_m[features]
    y_train_m = train_m[target]

    X_test_m = test_m[features]

    modele = Pipeline([
        (
            "scaler",
            StandardScaler(),
        ),
        (
            "model",
            RandomForestRegressor(
                n_estimators=150,
                random_state=42,
                n_jobs=-1,
            ),
        ),
    ])

    modele.fit(
        X_train_m,
        y_train_m,
    )

    predictions = modele.predict(
        X_test_m
    )

    pred_par_marche[
        test.index.isin(test_m.index)
    ] = predictions

    modeles_marches[marche] = modele


coordonnees = {
    "Segou": (13.44, -6.26),
    "Bamako": (12.64, -8.00),
    "Mopti": (14.49, -4.19),
    "Sikasso": (11.32, -5.67),
    "Tombouctou": (16.77, -3.01),
}

df["latitude"] = df["marche"].map(
    lambda x: coordonnees[x][0]
)

df["longitude"] = df["marche"].map(
    lambda x: coordonnees[x][1]
)



train = df[
    df["date"] < date_test
].copy()

test = df[
    df["date"] >= date_test
].copy()


features_spatiales = features + [
    "latitude",
    "longitude",
]


X_train_spatial = train[
    features_spatiales
]

y_train_spatial = train[target]

X_test_spatial = test[
    features_spatiales
]

y_test_spatial = test[target]


modele_spatial = Pipeline([
    (
        "scaler",
        StandardScaler(),
    ),
    (
        "model",
        RandomForestRegressor(
            n_estimators=150,
            random_state=42,
            n_jobs=-1,
        ),
    ),
])


modele_spatial.fit(
    X_train_spatial,
    y_train_spatial,
)

pred_spatial = modele_spatial.predict(
    X_test_spatial
)


def evaluation(y_true, y_pred):

    rmse = np.sqrt(
        mean_squared_error(
            y_true,
            y_pred,
        )
    )

    mae = mean_absolute_error(
        y_true,
        y_pred,
    )

    mape = np.mean(
        np.abs(
            (y_true - y_pred)
            / y_true
        )
    ) * 100

    return rmse, mae, mape


rmse_global, mae_global, mape_global = evaluation(
    y_test,
    pred_global,
)

rmse_marche, mae_marche, mape_marche = evaluation(
    y_test,
    pred_par_marche,
)

rmse_spatial, mae_spatial, mape_spatial = evaluation(
    y_test_spatial,
    pred_spatial,
)


resultats = pd.DataFrame({
    "Modèle": [
        "Global",
        "1 modèle / marché",
        "Multi-task spatial",
    ],
    "RMSE": [
        rmse_global,
        rmse_marche,
        rmse_spatial,
    ],
    "MAE": [
        mae_global,
        mae_marche,
        mae_spatial,
    ],
    "MAPE (%)": [
        mape_global,
        mape_marche,
        mape_spatial,
    ],
})

print("\n=== COMPARAISON DES MODÈLES ===")
print(resultats.sort_values("RMSE"))



print("\n=== BACKTEST ===")

dates_max = sorted(
    df["date"].unique()
)

periodes = [
    (
        dates_max[-150],
        dates_max[-120],
    ),
    (
        dates_max[-120],
        dates_max[-90],
    ),
    (
        dates_max[-90],
        dates_max[-60],
    ),
]


backtest_resultats = []

for numero, (debut_test, fin_test) in enumerate(
    periodes,
    start=1,
):

    train_bt = df[
        df["date"] < debut_test
    ]

    test_bt = df[
        (df["date"] >= debut_test)
        & (df["date"] < fin_test)
    ]

    X_train_bt = train_bt[
        features_spatiales
    ]

    y_train_bt = train_bt[target]

    X_test_bt = test_bt[
        features_spatiales
    ]

    y_test_bt = test_bt[target]

    modele_bt = Pipeline([
        (
            "scaler",
            StandardScaler(),
        ),
        (
            "model",
            RandomForestRegressor(
                n_estimators=100,
                random_state=42,
                n_jobs=-1,
            ),
        ),
    ])

    modele_bt.fit(
        X_train_bt,
        y_train_bt,
    )

    pred_bt = modele_bt.predict(
        X_test_bt
    )

    rmse_bt, mae_bt, mape_bt = evaluation(
        y_test_bt,
        pred_bt,
    )

    backtest_resultats.append({
        "Période": numero,
        "RMSE": rmse_bt,
        "MAE": mae_bt,
        "MAPE (%)": mape_bt,
    })


backtest_df = pd.DataFrame(
    backtest_resultats
)

print(backtest_df)


plt.figure(figsize=(12, 6))


test_sego = test[
    test["marche"] == "Segou"
].copy()

pred_sego = modele_spatial.predict(
    test_sego[features_spatiales]
)

plt.plot(
    test_sego["date"],
    test_sego["target_7j"],
    label="Prix réel à J+7",
)

plt.plot(
    test_sego["date"],
    pred_sego,
    label="Prédiction",
)

plt.title(
    "Prédiction du prix du mil à J+7 - Ségou"
)

plt.xlabel("Date")
plt.ylabel("Prix")

plt.legend()

plt.tight_layout()
plt.show()