import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.datasets import fetch_california_housing
from sklearn.ensemble import (
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


data = fetch_california_housing()

X = pd.DataFrame(
    data.data,
    columns=data.feature_names,
)

y = pd.Series(
    data.target,
    name="price",
)

print("=== APERÇU DES DONNÉES ===")
print(X.head())

print("\n=== DIMENSIONS ===")
print(f"X : {X.shape}")
print(f"y : {y.shape}")

print("\n=== INFORMATIONS ===")
print(X.info())

print("\n=== STATISTIQUES ===")
print(X.describe())

print("\n=== VALEURS MANQUANTES ===")
print(X.isnull().sum())

print("\n=== VARIABLE CIBLE ===")
print(y.describe())



X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
)

print("\n=== TRAIN / TEST ===")
print(f"Train : {X_train.shape}")
print(f"Test  : {X_test.shape}")



modeles = {
    "LinearRegression": LinearRegression(),

    "RandomForest": RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        n_jobs=-1,
    ),

    "GradientBoosting": GradientBoostingRegressor(
        n_estimators=100,
        random_state=42,
    ),
}


resultats = {}

for nom, modele in modeles.items():


    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("model", modele),
    ])

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)

    rmse = np.sqrt(
        mean_squared_error(y_test, y_pred)
    )

    r2 = r2_score(y_test, y_pred)

    resultats[nom] = {
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2,
        "pipeline": pipeline,
    }

    print(
        f"\n{nom}"
        f"\n  MAE  = {mae:.3f}"
        f"\n  RMSE = {rmse:.3f}"
        f"\n  R²   = {r2:.3f}"
    )





meilleur_nom = max(
    resultats,
    key=lambda nom: resultats[nom]["R2"],
)

meilleur_pipeline = resultats[meilleur_nom]["pipeline"]

print("\n=== MEILLEUR MODÈLE ===")
print(meilleur_nom)



meilleur_modele = resultats[meilleur_nom]["pipeline"].named_steps[
    "model"
]

if meilleur_nom == "RandomForest":

    param_grid = {
        "model__n_estimators": [100, 200],
        "model__max_depth": [None, 10, 20],
        "model__min_samples_split": [2, 5],
    }

elif meilleur_nom == "GradientBoosting":

    param_grid = {
        "model__n_estimators": [100, 200],
        "model__learning_rate": [0.05, 0.1],
        "model__max_depth": [2, 3, 4],
    }

else:

    param_grid = {
        "model__fit_intercept": [True, False],
    }


grid = GridSearchCV(
    estimator=Pipeline([
        ("scaler", StandardScaler()),
        ("model", meilleur_modele),
    ]),
    param_grid=param_grid,
    cv=5,
    scoring="r2",
    n_jobs=-1,
)

grid.fit(X_train, y_train)

print("\n=== GRIDSEARCH ===")
print("Meilleurs paramètres :")
print(grid.best_params_)

print(f"\nMeilleur score CV : {grid.best_score_:.3f}")



modele_final = grid.best_estimator_

y_pred = modele_final.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)

rmse = np.sqrt(
    mean_squared_error(y_test, y_pred)
)

r2 = r2_score(y_test, y_pred)

print("\n=== MODÈLE FINAL ===")
print(f"MAE  : {mae:.3f}")
print(f"RMSE : {rmse:.3f}")
print(f"R²   : {r2:.3f}")



modele = modele_final.named_steps["model"]

if hasattr(modele, "feature_importances_"):

    importances = modele.feature_importances_

    importance_df = pd.DataFrame({
        "feature": X.columns,
        "importance": importances,
    })

    importance_df = importance_df.sort_values(
        by="importance",
        ascending=False,
    )

    print("\n=== IMPORTANCE DES FEATURES ===")
    print(importance_df)

    # Graphique
    plt.figure(figsize=(10, 6))

    plt.barh(
        importance_df["feature"],
        importance_df["importance"],
    )

    plt.xlabel("Importance")
    plt.ylabel("Feature")
    plt.title("Importance des features")

    plt.gca().invert_yaxis()

    plt.tight_layout()
    plt.show()

else:
    print(
        "\nLe modèle choisi ne possède pas "
        "d'attribut feature_importances_."
    )



plt.figure(figsize=(8, 6))

plt.scatter(
    y_test,
    y_pred,
    alpha=0.5,
)

minimum = min(y_test.min(), y_pred.min())
maximum = max(y_test.max(), y_pred.max())

plt.plot(
    [minimum, maximum],
    [minimum, maximum],
    linestyle="--",
)

plt.xlabel("Valeurs réelles (y_test)")
plt.ylabel("Valeurs prédites (y_pred)")
plt.title("Valeurs réelles vs prédictions")

plt.tight_layout()
plt.show()


joblib.dump(
    modele_final,
    "california_housing_model.joblib",
)

print(
    "\nModèle sauvegardé dans : "
    "california_housing_model.joblib"
)



modele_charge = joblib.load(
    "california_housing_model.joblib"
)

predictions = modele_charge.predict(
    X_test.head()
)

print("\n=== TEST DU MODÈLE SAUVEGARDÉ ===")
print(predictions)