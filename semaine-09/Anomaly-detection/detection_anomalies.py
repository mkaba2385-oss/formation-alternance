import os

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from keras import Input, Sequential
from keras.layers import Dense
from sklearn.ensemble import IsolationForest
from sklearn.metrics import (
    average_precision_score,
    classification_report,
    precision_recall_curve,
)
from sklearn.preprocessing import StandardScaler
from sklearn.svm import OneClassSVM


rng = np.random.default_rng(42)

n_points = 1000
n_anomalies = int(n_points * 0.05)
n_normaux = n_points - n_anomalies

normal = rng.normal(
    loc=0,
    scale=1,
    size=(n_normaux, 2),
)

anomalies = rng.normal(
    loc=5,
    scale=1,
    size=(n_anomalies, 2),
)


X = np.vstack([normal, anomalies])

y = np.concatenate([
    np.zeros(n_normaux),
    np.ones(n_anomalies),
])


indices = rng.permutation(len(X))

X = X[indices]
y = y[indices]


print(f"Nombre total de points : {len(X)}")
print(f"Points normaux : {(y == 0).sum()}")
print(f"Anomalies : {(y == 1).sum()}")




scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)



isolation_forest = IsolationForest(
    contamination=0.05,
    random_state=42,
)

isolation_forest.fit(X_scaled)


pred_if = isolation_forest.predict(X_scaled)


pred_if = np.where(pred_if == -1, 1, 0)


print("\n===== Isolation Forest =====")

print(
    classification_report(
        y,
        pred_if,
        target_names=["Normal", "Anomalie"],
        zero_division=0,
    )
)



one_class_svm = OneClassSVM(
    kernel="rbf",
    nu=0.05,
    gamma="scale",
)

one_class_svm.fit(X_scaled)


pred_svm = one_class_svm.predict(X_scaled)


pred_svm = np.where(pred_svm == -1, 1, 0)


print("\n===== One-Class SVM =====")

print(
    classification_report(
        y,
        pred_svm,
        target_names=["Normal", "Anomalie"],
        zero_division=0,
    )
)



autoencoder = Sequential([
    Input(shape=(2,)),
    Dense(8, activation="relu"),
    Dense(2, activation="relu"),
    Dense(8, activation="relu"),
    Dense(2, activation="linear"),
])

autoencoder.compile(
    optimizer="adam",
    loss="mse",
)


X_normal = X_scaled[y == 0]

autoencoder.fit(
    X_normal,
    X_normal,
    epochs=30,
    batch_size=32,
    verbose=0,
)



X_reconstructed = autoencoder.predict(
    X_scaled,
    verbose=0,
)

reconstruction_error = np.mean(
    np.square(X_scaled - X_reconstructed),
    axis=1,
)


normal_errors = reconstruction_error[y == 0]

threshold = np.percentile(
    normal_errors,
    95,
)

pred_autoencoder = (
    reconstruction_error > threshold
).astype(int)


print("\n===== Autoencoder =====")

print(f"Seuil : {threshold:.4f}")

print(
    classification_report(
        y,
        pred_autoencoder,
        target_names=["Normal", "Anomalie"],
        zero_division=0,
    )
)



scores_if = -isolation_forest.decision_function(
    X_scaled
)

scores_svm = -one_class_svm.decision_function(
    X_scaled
)

scores_autoencoder = reconstruction_error


def afficher_precision_recall(
    y_true: np.ndarray,
    scores: np.ndarray,
    nom: str,
) -> None:
    """Affiche la courbe Precision-Recall d'un modèle."""

    precision, recall, _ = precision_recall_curve(
        y_true,
        scores,
    )

    average_precision = average_precision_score(
        y_true,
        scores,
    )

    plt.plot(
        recall,
        precision,
        label=f"{nom} (AP={average_precision:.3f})",
    )


plt.figure(figsize=(8, 6))

afficher_precision_recall(
    y,
    scores_if,
    "Isolation Forest",
)

afficher_precision_recall(
    y,
    scores_svm,
    "One-Class SVM",
)

afficher_precision_recall(
    y,
    scores_autoencoder,
    "Autoencoder",
)

plt.xlabel("Recall")
plt.ylabel("Precision")

plt.title(
    "Precision-Recall - Détection d'anomalies"
)

plt.legend()
plt.grid()

plt.show()