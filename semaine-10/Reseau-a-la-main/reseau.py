import numpy as np

X = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
], dtype=float)

y = np.array([
    [0],
    [1],
    [1],
    [0]
], dtype=float)

np.random.seed(42)

W1 = np.random.randn(2, 3) * 0.5
b1 = np.zeros((1, 3))

W2 = np.random.randn(3, 1) * 0.5
b2 = np.zeros((1, 1))


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def sigmoid_derivative(a):
    return a * (1 - a)


def relu(z):
    return np.maximum(0, z)


def relu_derivative(z):
    return (z > 0).astype(float)


learning_rate = 0.1
epochs = 10000

for epoch in range(epochs):

    z1 = X @ W1 + b1
    a1 = relu(z1)

    z2 = a1 @ W2 + b2
    y_pred = sigmoid(z2)

    epsilon = 1e-8

    loss = -np.mean(
        y * np.log(y_pred + epsilon)
        + (1 - y) * np.log(1 - y_pred + epsilon)
    )

    m = X.shape[0]

    dz2 = (y_pred - y) / m

    dW2 = a1.T @ dz2
    db2 = np.sum(dz2, axis=0, keepdims=True)

    da1 = dz2 @ W2.T

    dz1 = da1 * relu_derivative(z1)

    dW1 = X.T @ dz1
    db1 = np.sum(dz1, axis=0, keepdims=True)

    W2 -= learning_rate * dW2
    b2 -= learning_rate * db2

    W1 -= learning_rate * dW1
    b1 -= learning_rate * db1

    if epoch % 1000 == 0:
        print(f"Epoch {epoch:5d} | Loss = {loss:.6f}")


z1 = X @ W1 + b1
a1 = relu(z1)

z2 = a1 @ W2 + b2
y_pred = sigmoid(z2)

print("\nRésultats :")
print("-----------------------")

for inputs, prediction, target in zip(X, y_pred, y):
    print(
        f"{inputs.astype(int)} "
        f"-> prédiction = {prediction[0]:.4f} "
        f"| attendu = {int(target[0])}"
    )

predictions = (y_pred >= 0.5).astype(int)

print("\nClasses prédites :")
print(predictions.ravel())

print("\nClasses attendues :")
print(y.ravel())