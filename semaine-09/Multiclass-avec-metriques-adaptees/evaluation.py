import numpy as np
import pandas as pd

from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    f1_score,
)

from xgboost import XGBClassifier


# 1. Charger le dataset

digits = load_digits()

X = digits.data
y = digits.target


# Créer un dataset déséquilibré

rng = np.random.default_rng(42)

indices = []

for classe in np.unique(y):
    classe_indices = np.where(y == classe)[0]

    if classe in [0, 1, 2]:
        n = int(len(classe_indices) * 0.25)
    elif classe in [3, 4]:
        n = int(len(classe_indices) * 0.50)
    else:
        n = len(classe_indices)

    selection = rng.choice(
        classe_indices,
        size=n,
        replace=False,
    )

    indices.extend(selection)


indices = np.array(indices)

X = X[indices]
y = y[indices]


print("Répartition des classes :")
print(pd.Series(y).value_counts().sort_index())


# Séparer train / test

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)


# Définir les 3 classifieurs

modeles = {
    "Logistic Regression": Pipeline([
        ("scaler", StandardScaler()),
        (
            "model",
            LogisticRegression(
                max_iter=2000,
                random_state=42,
            ),
        ),
    ]),
    "Random Forest": RandomForestClassifier(
        n_estimators=200,
        random_state=42,
    ),
    "XGBoost": XGBClassifier(
        n_estimators=200,
        max_depth=5,
        learning_rate=0.1,
        objective="multi:softmax",
        num_class=10,
        eval_metric="mlogloss",
        random_state=42,
    ),
}


# Entraîner et évaluer les modèles

for nom, modele in modeles.items():

    print("\n" + "=" * 60)
    print(nom)
    print("=" * 60)

  
    modele.fit(X_train, y_train)


    y_pred = modele.predict(X_test)

    # Classification report

    print("\nClassification report :")
    print(
        classification_report(
            y_test,
            y_pred,
            zero_division=0,
        )
    )


    macro_f1 = f1_score(
        y_test,
        y_pred,
        average="macro",
    )

    print(f"Macro-F1 : {macro_f1:.3f}")


    print("\nMatrice de confusion :")
    print(confusion_matrix(y_test, y_pred))


    report = classification_report(
        y_test,
        y_pred,
        output_dict=True,
        zero_division=0,
    )

    f1_par_classe = {
        int(classe): valeurs["f1-score"]
        for classe, valeurs in report.items()
        if classe.isdigit()
    }

    classe_difficile = min(
        f1_par_classe,
        key=f1_par_classe.get,
    )

    print(
        f"\nClasse la plus difficile : "
        f"{classe_difficile} "
        f"(F1 = {f1_par_classe[classe_difficile]:.3f})"
    )