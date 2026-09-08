import joblib
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.datasets import fetch_california_housing
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor


# Charger le dataset

housing = fetch_california_housing(as_frame=True)

df = housing.frame.copy()

print("Dimensions :", df.shape)
print(df.head())


# Ajouter une variable catégorielle

df["income_category"] = pd.cut(
    df["MedInc"],
    bins=[-np.inf, 2, 4, 6, np.inf],
    labels=["low", "medium", "high", "very_high"],
)


# Séparer X et y

X = df.drop(columns=["MedHouseVal"])
y = df["MedHouseVal"]

print("\nVariables X :")
print(X.columns.tolist())

print("\nVariable cible :", y.name)


# Train / Test split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
)

print("\nTaille entraînement :", X_train.shape)
print("Taille test :", X_test.shape)


# Définir les colonnes

numeric_features = [
    "MedInc",
    "HouseAge",
    "AveRooms",
    "AveBedrms",
    "Population",
    "AveOccup",
    "Latitude",
    "Longitude",
]

categorical_features = [
    "income_category",
]


# Pipeline numérique

numeric_pipeline = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="median"),
        ),
        (
            "scaler",
            StandardScaler(),
        ),
    ]
)



# Pipeline catégoriel

categorical_pipeline = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="most_frequent"),
        ),
        (
            "encoder",
            OneHotEncoder(
                handle_unknown="ignore",
            ),
        ),
    ]
)



# ColumnTransformer

preprocessor = ColumnTransformer(
    transformers=[
        (
            "numeric",
            numeric_pipeline,
            numeric_features,
        ),
        (
            "categorical",
            categorical_pipeline,
            categorical_features,
        ),
    ]
)


# Pipeline complet
# Le preprocessing est exécuté avant le modèle

pipeline = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor,
        ),
        (
            "model",
            RandomForestRegressor(
                random_state=42,
                n_jobs=-1,
            ),
        ),
    ]
)


# Entraîner le pipeline

pipeline.fit(X_train, y_train)

print("\nPipeline entraîné avec succès.")


# Faire des prédictions

y_pred = pipeline.predict(X_test)


# Évaluer le modèle

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("\n===== Résultats du modèle =====")
print(f"MAE  : {mae:.4f}")
print(f"RMSE : {rmse:.4f}")
print(f"R²   : {r2:.4f}")


# GridSearchCV
# On cherche les meilleurs hyperparamètres du Random Forest.

param_grid = {
    "model__n_estimators": [
        100,
        200,
    ],
    "model__max_depth": [
        None,
        10,
        20,
    ],
    "model__min_samples_split": [
        2,
        5,
    ],
}


grid_search = GridSearchCV(
    estimator=pipeline,
    param_grid=param_grid,
    cv=3,
    scoring="neg_root_mean_squared_error",
    n_jobs=-1,
    verbose=1,
)


# Lancer le GridSearch

grid_search.fit(X_train, y_train)


# Afficher les meilleurs paramètres

print("\n===== GridSearchCV =====")

print("\nMeilleurs paramètres :")
print(grid_search.best_params_)

print("\nMeilleur score CV :")
print(-grid_search.best_score_)


# Évaluer le meilleur pipeline sur le test

best_model = grid_search.best_estimator_

y_pred_best = best_model.predict(X_test)

mae_best = mean_absolute_error(
    y_test,
    y_pred_best,
)

rmse_best = np.sqrt(
    mean_squared_error(
        y_test,
        y_pred_best,
    )
)

r2_best = r2_score(
    y_test,
    y_pred_best,
)

print("\n===== Meilleur modèle =====")
print(f"MAE  : {mae_best:.4f}")
print(f"RMSE : {rmse_best:.4f}")
print(f"R²   : {r2_best:.4f}")


# Sérialiser le pipeline avec joblib

model_path = "california_housing_pipeline.joblib"

joblib.dump(
    best_model,
    model_path,
)

print(f"\nPipeline sauvegardé dans : {model_path}")


# Recharger le modèle

loaded_model = joblib.load(
    model_path,
)

print("Pipeline rechargé avec succès.")


# Tester le modèle rechargé

sample = X_test.iloc[[0]]

prediction = loaded_model.predict(sample)

print("\n===== Test du modèle sauvegardé =====")
print("Valeur réelle :", y_test.iloc[0])
print("Prédiction     :", prediction[0])