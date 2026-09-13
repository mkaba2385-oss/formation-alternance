import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim


np.random.seed(42)
torch.manual_seed(42)


X = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
], dtype=np.float64)

y = np.array([
    [0],
    [1],
    [1],
    [0]
], dtype=np.float64)


def relu(z):
    return np.maximum(0, z)


def relu_derivative(z):
    return (z > 0).astype(float)


def sigmoid(z):
    z = np.clip(z, -500, 500)
    return 1 / (1 + np.exp(-z))


class MLP:

    def __init__(
        self,
        input_dim,
        hidden_dim,
        output_dim,
        lr=0.1,
        momentum=0.9
    ):
        self.lr = lr
        self.momentum = momentum

        self.W1 = np.random.randn(
            input_dim,
            hidden_dim
        ) * np.sqrt(2 / input_dim)

        self.b1 = np.zeros((1, hidden_dim))

        self.W2 = np.random.randn(
            hidden_dim,
            output_dim
        ) * np.sqrt(2 / hidden_dim)

        self.b2 = np.zeros((1, output_dim))

        self.vW1 = np.zeros_like(self.W1)
        self.vb1 = np.zeros_like(self.b1)

        self.vW2 = np.zeros_like(self.W2)
        self.vb2 = np.zeros_like(self.b2)

    def forward(self, X):
        self.z1 = X @ self.W1 + self.b1
        self.a1 = relu(self.z1)

        self.z2 = self.a1 @ self.W2 + self.b2
        self.a2 = sigmoid(self.z2)

        return self.a2

    def loss(self, y_pred, y):
        epsilon = 1e-8

        return -np.mean(
            y * np.log(y_pred + epsilon)
            + (1 - y) * np.log(1 - y_pred + epsilon)
        )

    def backward(self, X, y, y_pred):
        m = X.shape[0]

        dz2 = (y_pred - y) / m

        self.dW2 = self.a1.T @ dz2
        self.db2 = np.sum(
            dz2,
            axis=0,
            keepdims=True
        )

        da1 = dz2 @ self.W2.T

        dz1 = da1 * relu_derivative(self.z1)

        self.dW1 = X.T @ dz1
        self.db1 = np.sum(
            dz1,
            axis=0,
            keepdims=True
        )

    def update(self):
        self.vW1 = (
            self.momentum * self.vW1
            - self.lr * self.dW1
        )

        self.vb1 = (
            self.momentum * self.vb1
            - self.lr * self.db1
        )

        self.vW2 = (
            self.momentum * self.vW2
            - self.lr * self.dW2
        )

        self.vb2 = (
            self.momentum * self.vb2
            - self.lr * self.db2
        )

        self.W1 += self.vW1
        self.b1 += self.vb1

        self.W2 += self.vW2
        self.b2 += self.vb2

    def predict_proba(self, X):
        return self.forward(X)

    def predict(self, X):
        return (
            self.predict_proba(X) >= 0.5
        ).astype(int)


numpy_model = MLP(
    input_dim=2,
    hidden_dim=4,
    output_dim=1,
    lr=0.1,
    momentum=0.9
)


epochs = 10000
numpy_losses = []


for epoch in range(epochs):

    y_pred = numpy_model.forward(X)

    loss = numpy_model.loss(
        y_pred,
        y
    )

    numpy_model.backward(
        X,
        y,
        y_pred
    )

    numpy_model.update()

    numpy_losses.append(loss)

    if epoch % 1000 == 0:
        print(
            f"NumPy Epoch {epoch} "
            f"| Loss = {loss:.6f}"
        )


numpy_probabilities = numpy_model.predict_proba(X)
numpy_predictions = numpy_model.predict(X)

numpy_accuracy = np.mean(
    numpy_predictions == y
)


print("\nRésultats NumPy")

for i in range(len(X)):
    print(
        X[i].astype(int),
        "->",
        f"{numpy_probabilities[i, 0]:.4f}",
        "| prédiction:",
        numpy_predictions[i, 0],
        "| attendu:",
        int(y[i, 0])
    )


print(
    f"Accuracy NumPy : "
    f"{numpy_accuracy * 100:.2f}%"
)


X_torch = torch.tensor(
    X,
    dtype=torch.float32
)

y_torch = torch.tensor(
    y,
    dtype=torch.float32
)


class TorchMLP(nn.Module):

    def __init__(self):
        super().__init__()

        self.layer1 = nn.Linear(2, 4)
        self.relu = nn.ReLU()
        self.layer2 = nn.Linear(4, 1)

    def forward(self, X):
        X = self.layer1(X)
        X = self.relu(X)
        X = self.layer2(X)
        return X


torch_model = TorchMLP()

criterion = nn.BCEWithLogitsLoss()

optimizer = optim.SGD(
    torch_model.parameters(),
    lr=0.1,
    momentum=0.9
)

torch_losses = []


for epoch in range(epochs):

    optimizer.zero_grad()

    logits = torch_model(X_torch)

    loss = criterion(
        logits,
        y_torch
    )

    loss.backward()

    optimizer.step()

    torch_losses.append(
        loss.item()
    )

    if epoch % 1000 == 0:
        print(
            f"PyTorch Epoch {epoch} "
            f"| Loss = {loss.item():.6f}"
        )


with torch.no_grad():

    logits = torch_model(X_torch)

    torch_probabilities = torch.sigmoid(
        logits
    )

    torch_predictions = (
        torch_probabilities >= 0.5
    ).int()


torch_accuracy = (
    torch_predictions.numpy()
    == y
).mean()


print("\nRésultats PyTorch")

for i in range(len(X)):
    print(
        X[i].astype(int),
        "->",
        f"{torch_probabilities[i, 0].item():.4f}",
        "| prédiction:",
        torch_predictions[i, 0].item(),
        "| attendu:",
        int(y[i, 0])
    )


print(
    f"Accuracy PyTorch : "
    f"{torch_accuracy * 100:.2f}%"
)


plt.figure(figsize=(10, 5))

plt.plot(
    numpy_losses,
    label="NumPy"
)

plt.plot(
    torch_losses,
    label="PyTorch"
)

plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("MLP XOR - NumPy vs PyTorch")
plt.legend()
plt.grid()

plt.show()