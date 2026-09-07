import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression, Ridge



# Dataset

X = np.array([
    [30],
    [40],
    [50],
    [60],
    [70],
    [80],
    [90],
    [100],
], dtype=float)

y = np.array([
    100,
    130,
    160,
    190,
    220,
    250,
    280,
    310,
], dtype=float)


# Fonction de coût

def mse(
    y_true: np.ndarray,
    y_pred: np.ndarray,
) -> float:
    return float(np.mean((y_true - y_pred) ** 2))


# Closed-form

def normal_equation(
    X: np.ndarray,
    y: np.ndarray,
) -> np.ndarray:

    X_b = np.c_[
        np.ones((X.shape[0], 1)),
        X,
    ]

    theta = (
        np.linalg.inv(X_b.T @ X_b)
        @ X_b.T
        @ y
    )

    return theta


# Batch Gradient Descent

def batch_gradient_descent(
    X: np.ndarray,
    y: np.ndarray,
    learning_rate: float = 0.1,
    epochs: int = 1000,
) -> tuple[float, float, list[float]]:

    n = len(X)

    w = 0.0
    b = 0.0

    history = []

    for _ in range(epochs):

        predictions = w * X + b

        errors = predictions - y

        dw = (
            2
            / n
            * np.sum(X * errors)
        )

        db = (
            2
            / n
            * np.sum(errors)
        )

        w -= learning_rate * dw
        b -= learning_rate * db

        history.append(
            mse(y, predictions)
        )

    return w, b, history


# SGD

def stochastic_gradient_descent(
    X: np.ndarray,
    y: np.ndarray,
    learning_rate: float = 0.01,
    epochs: int = 100,
    seed: int = 42,
) -> tuple[float, float, list[float]]:

    rng = np.random.default_rng(seed)

    w = 0.0
    b = 0.0

    history = []

    for _ in range(epochs):

        indices = rng.permutation(len(X))

        for i in indices:

            xi = X[i]
            yi = y[i]

            prediction = w * xi + b

            error = prediction - yi

            dw = 2 * xi * error
            db = 2 * error

            w -= learning_rate * dw
            b -= learning_rate * db

        predictions = w * X + b

        history.append(
            mse(y, predictions)
        )

    return w, b, history


# Closed-form

theta = normal_equation(
    X,
    y,
)

b_closed = theta[0]
w_closed = theta[1]

predictions_closed = (
    w_closed * X.ravel()
    + b_closed
)

loss_closed = mse(
    y,
    predictions_closed,
)


# Standardisation pour GD / SGD

X_flat = X.ravel()

X_mean = X_flat.mean()
X_std = X_flat.std()

X_scaled = (
    X_flat - X_mean
) / X_std


# Batch GD

w_gd, b_gd, history_gd = (
    batch_gradient_descent(
        X_scaled,
        y,
        learning_rate=0.1,
        epochs=1000,
    )
)

w_gd_original = w_gd / X_std

b_gd_original = (
    b_gd
    - w_gd * X_mean / X_std
)


# SGD

w_sgd, b_sgd, history_sgd = (
    stochastic_gradient_descent(
        X_scaled,
        y,
        learning_rate=0.01,
        epochs=100,
        seed=42,
    )
)

w_sgd_original = w_sgd / X_std

b_sgd_original = (
    b_sgd
    - w_sgd * X_mean / X_std
)


# Sklearn

model = LinearRegression()

model.fit(X, y)


# Résultats

print("\n=== RÉSULTATS ===")

print(
    f"Closed-form : "
    f"w={w_closed:.6f}, "
    f"b={b_closed:.6f}"
)

print(
    f"Batch GD    : "
    f"w={w_gd_original:.6f}, "
    f"b={b_gd_original:.6f}"
)

print(
    f"SGD         : "
    f"w={w_sgd_original:.6f}, "
    f"b={b_sgd_original:.6f}"
)

print(
    f"Sklearn     : "
    f"w={model.coef_[0]:.6f}, "
    f"b={model.intercept_:.6f}"
)

print("\n=== ERREURS ===")

print(
    "Closed-form MSE :",
    loss_closed,
)

print(
    "Sklearn MSE :",
    mse(y, model.predict(X)),
)



# Courbe de convergence

plt.figure(figsize=(8, 5))

plt.plot(
    history_gd,
    label="Batch Gradient Descent",
)

plt.plot(
    history_sgd,
    label="SGD",
)

plt.axhline(
    loss_closed,
    linestyle="--",
    label="Closed-form",
)

plt.xlabel("Époque")
plt.ylabel("MSE")
plt.title(
    "Comparaison de la convergence"
)

plt.legend()
plt.grid(True)

plt.show()


# Régression sur le dataset


plt.figure(figsize=(8, 5))

plt.scatter(
    X,
    y,
    label="Données",
)

x_line = np.linspace(
    30,
    100,
    100,
)

y_line = (
    w_closed * x_line
    + b_closed
)

plt.plot(
    x_line,
    y_line,
    label="Régression linéaire",
)

plt.xlabel("Surface (m²)")
plt.ylabel("Prix (k€)")
plt.title(
    "Régression linéaire : surface → prix"
)

plt.legend()
plt.grid(True)

plt.show()