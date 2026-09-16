import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from IPython.display import display
import pandas as pd
import time

device = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Device utilisé : {device}")

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
])

train_ds = datasets.MNIST(
    "./data",
    train=True,
    download=True,
    transform=transform
)

test_ds = datasets.MNIST(
    "./data",
    train=False,
    download=True,
    transform=transform
)

print(f"Train : {len(train_ds)} images")
print(f"Test : {len(test_ds)} images")


class MLP(nn.Module):

    def __init__(self, dropout=0.3):
        super().__init__()

        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(28 * 28, 256)
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, 10)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):

        x = self.flatten(x)
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = F.relu(self.fc2(x))
        x = self.dropout(x)

        return self.fc3(x)


def train_epoch(model, loader, optimizer, loss_fn):

    model.train()

    total_loss = 0
    correct = 0

    for x, y in loader:

        x = x.to(device)
        y = y.to(device)

        logits = model(x)
        loss = loss_fn(logits, y)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item() * x.size(0)

        correct += (
            (logits.argmax(dim=1) == y)
            .sum()
            .item()
        )

    avg_loss = total_loss / len(loader.dataset)
    accuracy = correct / len(loader.dataset)

    return avg_loss, accuracy


def evaluate(model, loader, loss_fn):

    model.eval()

    total_loss = 0
    correct = 0

    with torch.no_grad():

        for x, y in loader:

            x = x.to(device)
            y = y.to(device)

            logits = model(x)
            loss = loss_fn(logits, y)

            total_loss += loss.item() * x.size(0)

            correct += (
                (logits.argmax(dim=1) == y)
                .sum()
                .item()
            )

    avg_loss = total_loss / len(loader.dataset)
    accuracy = correct / len(loader.dataset)

    return avg_loss, accuracy


def run_experiment(
    name,
    learning_rate=1e-3,
    dropout=0.3,
    batch_size=64,
    epochs=10
):

    print("\n" + "=" * 70)
    print(f"EXPÉRIENCE : {name}")
    print("=" * 70)

    print(f"Learning rate : {learning_rate}")
    print(f"Dropout : {dropout}")
    print(f"Batch size : {batch_size}")
    print(f"Epochs : {epochs}")

    train_loader = DataLoader(
        train_ds,
        batch_size=batch_size,
        shuffle=True
    )

    test_loader = DataLoader(
        test_ds,
        batch_size=batch_size,
        shuffle=False
    )

    model = MLP(dropout=dropout).to(device)

    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=learning_rate
    )

    loss_fn = nn.CrossEntropyLoss()

    start_time = time.time()

    for epoch in range(1, epochs + 1):

        train_loss, train_acc = train_epoch(
            model,
            train_loader,
            optimizer,
            loss_fn
        )

        test_loss, test_acc = evaluate(
            model,
            test_loader,
            loss_fn
        )

        print(
            f"Epoch {epoch:2d}/{epochs} | "
            f"train_loss={train_loss:.4f} | "
            f"train_acc={train_acc:.3f} | "
            f"test_loss={test_loss:.4f} | "
            f"test_acc={test_acc:.3f}"
        )

    elapsed = time.time() - start_time

    print(f"\nTemps : {elapsed:.1f} secondes")
    print(f"Train accuracy finale : {train_acc * 100:.2f}%")
    print(f"Test accuracy finale : {test_acc * 100:.2f}%")

    return {
        "expérience": name,
        "learning_rate": learning_rate,
        "dropout": dropout,
        "batch_size": batch_size,
        "train_acc": train_acc,
        "test_acc": test_acc,
        "temps_sec": elapsed
    }


results = []

results.append(
    run_experiment(
        name="Baseline",
        learning_rate=1e-3,
        dropout=0.3,
        batch_size=64,
        epochs=10
    )
)

results.append(
    run_experiment(
        name="LR = 1e-2",
        learning_rate=1e-2,
        dropout=0.3,
        batch_size=64,
        epochs=10
    )
)

results.append(
    run_experiment(
        name="LR = 1e-4",
        learning_rate=1e-4,
        dropout=0.3,
        batch_size=64,
        epochs=10
    )
)

results.append(
    run_experiment(
        name="Dropout = 0.5",
        learning_rate=1e-3,
        dropout=0.5,
        batch_size=64,
        epochs=10
    )
)

results.append(
    run_experiment(
        name="Sans dropout",
        learning_rate=1e-3,
        dropout=0.0,
        batch_size=64,
        epochs=10
    )
)

results.append(
    run_experiment(
        name="Batch size = 256",
        learning_rate=1e-3,
        dropout=0.3,
        batch_size=256,
        epochs=10
    )
)

df_results = pd.DataFrame(results)

df_results["train_acc_%"] = df_results["train_acc"] * 100
df_results["test_acc_%"] = df_results["test_acc"] * 100

df_results = df_results[
    [
        "expérience",
        "learning_rate",
        "dropout",
        "batch_size",
        "train_acc_%",
        "test_acc_%",
        "temps_sec"
    ]
]

print("\n")
print("=" * 70)
print("RÉSULTATS FINAUX")
print("=" * 70)

display(df_results.round(2))