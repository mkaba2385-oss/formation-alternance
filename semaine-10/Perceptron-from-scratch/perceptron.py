import numpy as np
import matplotlib.pyplot as plt


class Perceptron:

    def __init__(self, input_dim, lr=0.01):
        self.weights = np.zeros(input_dim)
        self.bias = 0.0
        self.lr = lr
        self.gradient_weights = np.zeros(input_dim)
        self.gradient_bias = 0.0

    def forward(self, X):
        z = X @ self.weights + self.bias
        return (z >= 0).astype(int)

    def backward(self, X, y, predictions):
        error = y - predictions
        self.gradient_weights = X.T @ error
        self.gradient_bias = np.sum(error)

    def update(self):
        self.weights += self.lr * self.gradient_weights
        self.bias += self.lr * self.gradient_bias


X = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
], dtype=float)

y = np.array([0, 0, 0, 1])

perceptron = Perceptron(input_dim=2, lr=0.1)

epochs = 10

plt.figure(figsize=(8, 6))

for epoch in range(epochs):

    predictions = perceptron.forward(X)

    perceptron.backward(X, y, predictions)

    perceptron.update()

    plt.clf()

    for i in range(len(X)):
        if y[i] == 0:
            plt.scatter(X[i, 0], X[i, 1], marker="o", s=100)
        else:
            plt.scatter(X[i, 0], X[i, 1], marker="x", s=100)

    x_values = np.linspace(-0.2, 1.2, 100)

    if perceptron.weights[1] != 0:
        y_values = (
            -(perceptron.weights[0] * x_values + perceptron.bias)
            / perceptron.weights[1]
        )
        plt.plot(x_values, y_values)

    plt.xlim(-0.2, 1.2)
    plt.ylim(-0.2, 1.2)
    plt.xlabel("x1")
    plt.ylabel("x2")
    plt.title(f"Epoch {epoch + 1}")
    plt.grid(True)
    plt.pause(0.5)

plt.show()

print("Poids :", perceptron.weights)
print("Biais :", perceptron.bias)
print("Prédictions :", perceptron.forward(X))
print("Attendu :", y)