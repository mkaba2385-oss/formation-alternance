import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier


# 1. Chargement des données

df = pd.read_csv("titanic.csv")


# 2. Sélection des features et de la target


X = df.drop("Survived", axis=1)
y = df["Survived"]


# 3. Séparation train / test

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)


# 4. Baseline : toujours prédire la classe majoritaire

majority_class = y_train.mode()[0]

baseline_predictions = [majority_class] * len(y_test)

baseline_accuracy = accuracy_score(
    y_test,
    baseline_predictions,
)

baseline_precision = precision_score(
    y_test,
    baseline_predictions,
    zero_division=0,
)

baseline_recall = recall_score(
    y_test,
    baseline_predictions,
    zero_division=0,
)

baseline_f1 = f1_score(
    y_test,
    baseline_predictions,
    zero_division=0,
)


# 5. Préparation des données

numeric_features = [
    "Pclass",
    "Age",
    "SibSp",
    "Parch",
    "Fare",
]

categorical_features = [
    "Sex",
    "Embarked",
]


numeric_transformer = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median")),
    ]
)


categorical_transformer = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="most_frequent"),
        ),
        (
            "onehot",
            OneHotEncoder(handle_unknown="ignore"),
        ),
    ]
)


preprocessor = ColumnTransformer(
    transformers=[
        (
            "num",
            numeric_transformer,
            numeric_features,
        ),
        (
            "cat",
            categorical_transformer,
            categorical_features,
        ),
    ]
)


# 6. Définition des modèles

models = {
    "LogisticRegression": LogisticRegression(
        max_iter=1000,
        random_state=42,
    ),
    "DecisionTree": DecisionTreeClassifier(
        max_depth=5,
        random_state=42,
    ),
    "RandomForest": RandomForestClassifier(
        n_estimators=100,
        max_depth=5,
        random_state=42,
    ),
}


# 7. Entraînement et évaluation

results = []


# Résultat de la baseline
results.append(
    {
        "Model": "Baseline",
        "Accuracy": baseline_accuracy,
        "Precision": baseline_precision,
        "Recall": baseline_recall,
        "F1": baseline_f1,
    }
)


for name, model in models.items():

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model),
        ]
    )

    pipeline.fit(X_train, y_train)

    predictions = pipeline.predict(X_test)

    results.append(
        {
            "Model": name,
            "Accuracy": accuracy_score(
                y_test,
                predictions,
            ),
            "Precision": precision_score(
                y_test,
                predictions,
                zero_division=0,
            ),
            "Recall": recall_score(
                y_test,
                predictions,
                zero_division=0,
            ),
            "F1": f1_score(
                y_test,
                predictions,
                zero_division=0,
            ),
        }
    )


# 8. Affichage des résultats

results_df = pd.DataFrame(results)

print("\nRésultats :")
print(
    results_df.to_string(
        index=False,
        float_format=lambda x: f"{x:.3f}",
    )
)