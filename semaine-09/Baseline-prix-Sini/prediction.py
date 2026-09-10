import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error



np.random.seed(42)

dates = pd.date_range(
    start="2026-01-01",
    periods=180,
    freq="D",
)

prix_depart = 250

tendance = np.linspace(0, 30, 180)
bruit = np.random.normal(0, 8, 180)

prix = prix_depart + tendance + bruit


prix = np.maximum(prix, 50)

df = pd.DataFrame({
    "date": dates,
    "prix": prix,
})

df = df.set_index("date")

print(df.head())
print(df.tail())



plt.figure(figsize=(12, 5))

plt.plot(df.index, df["prix"])

plt.title("Prix quotidien du mil à Ségou")
plt.xlabel("Date")
plt.ylabel("Prix")

plt.tight_layout()
plt.show()


train = df.iloc[:-30].copy()
test = df.iloc[-30:].copy()

print("\nTaille train :", len(train))
print("Taille test  :", len(test))


def rmse(y_true, y_pred):
    return np.sqrt(
        mean_squared_error(y_true, y_pred)
    )


def mape(y_true, y_pred):
    return np.mean(
        np.abs((y_true - y_pred) / y_true)
    ) * 100



df["naive"] = df["prix"].shift(1)

test_naive = df.loc[test.index]

rmse_naive = rmse(
    test_naive["prix"],
    test_naive["naive"],
)

mape_naive = mape(
    test_naive["prix"],
    test_naive["naive"],
)

print("\n=== BASELINE NAIVE ===")
print(f"RMSE : {rmse_naive:.2f}")
print(f"MAPE : {mape_naive:.2f} %")



df["moving_average_7"] = (
    df["prix"]
    .shift(1)
    .rolling(7)
    .mean()
)

test_ma = df.loc[test.index]

test_ma = test_ma.dropna(
    subset=["moving_average_7"]
)

rmse_ma = rmse(
    test_ma["prix"],
    test_ma["moving_average_7"],
)

mape_ma = mape(
    test_ma["prix"],
    test_ma["moving_average_7"],
)

print("\n=== MOYENNE MOBILE 7 JOURS ===")
print(f"RMSE : {rmse_ma:.2f}")
print(f"MAPE : {mape_ma:.2f} %")


df_ridge = df[["prix"]].copy()

for lag in range(1, 8):
    df_ridge[f"lag_{lag}"] = (
        df_ridge["prix"].shift(lag)
    )

df_ridge = df_ridge.dropna()

print("\n=== DONNÉES RIDGE ===")
print(df_ridge.head())


train_ridge = df_ridge.iloc[:-30]
test_ridge = df_ridge.iloc[-30:]

features = [
    "lag_1",
    "lag_2",
    "lag_3",
    "lag_4",
    "lag_5",
    "lag_6",
    "lag_7",
]

X_train = train_ridge[features]
y_train = train_ridge["prix"]

X_test = test_ridge[features]
y_test = test_ridge["prix"]



model = Ridge(alpha=1.0)

model.fit(
    X_train,
    y_train,
)

y_pred_ridge = model.predict(X_test)



rmse_ridge = rmse(
    y_test,
    y_pred_ridge,
)

mape_ridge = mape(
    y_test,
    y_pred_ridge,
)

print("\n=== RIDGE ===")
print(f"RMSE : {rmse_ridge:.2f}")
print(f"MAPE : {mape_ridge:.2f} %")



resultats = pd.DataFrame({
    "Modèle": [
        "Naive",
        "Moyenne mobile 7 jours",
        "Ridge + lags",
    ],
    "RMSE": [
        rmse_naive,
        rmse_ma,
        rmse_ridge,
    ],
    "MAPE (%)": [
        mape_naive,
        mape_ma,
        mape_ridge,
    ],
})

print("\n=== COMPARAISON ===")
print(resultats)



plt.figure(figsize=(12, 6))

plt.plot(
    test.index,
    test["prix"],
    label="Prix réel",
)

plt.plot(
    test.index,
    test_naive["naive"],
    label="Naive",
)

plt.plot(
    test.index,
    test_ma["moving_average_7"],
    label="Moyenne mobile 7j",
)

plt.plot(
    test_ridge.index,
    y_pred_ridge,
    label="Ridge",
)

plt.title("Comparaison des prédictions")
plt.xlabel("Date")
plt.ylabel("Prix")

plt.legend()

plt.tight_layout()
plt.show()