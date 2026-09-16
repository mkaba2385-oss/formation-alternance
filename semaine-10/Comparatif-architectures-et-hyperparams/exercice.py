import time
import itertools
import copy

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms

import pandas as pd
import matplotlib.pyplot as plt


device = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Device utilisé : {device}")


transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
])


full_train_ds = datasets.MNIST(
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


train_size = 50000
val_size = 10000

train_ds, val_ds = random_split(
    full_train_ds,
    [train_size, val_size],
    generator=torch.Generator().manual_seed(42)
)


def create_loaders(batch_size=64):

    train_loader = DataLoader(
        train_ds,
        batch_size=batch_size,
        shuffle=True
    )

    val_loader = DataLoader(
        val_ds,
        batch_size=batch_size,
        shuffle=False
    )

    test_loader = DataLoader(
        test_ds,
        batch_size=batch_size,
        shuffle=False
    )

    return train_loader, val_loader, test_loader


class MLPShallow(nn.Module):

    def __init__(self):
        super().__init__()

        self.flatten = nn.Flatten()

        self.fc1 = nn.Linear(28 * 28, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):

        x = self.flatten(x)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)

        return x


class MLPDeep(nn.Module):

    def __init__(self):
        super().__init__()

        self.flatten = nn.Flatten()

        self.fc1 = nn.Linear(28 * 28, 512)
        self.fc2 = nn.Linear(512, 256)
        self.fc3 = nn.Linear(256, 128)
        self.fc4 = nn.Linear(128, 10)

    def forward(self, x):

        x = self.flatten(x)

        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))

        x = self.fc4(x)

        return x


class LeNet5(nn.Module):

    def __init__(self):
        super().__init__()

        self.conv1 = nn.Conv2d(1, 6, kernel_size=5)
        self.pool = nn.AvgPool2d(kernel_size=2)

        self.conv2 = nn.Conv2d(6, 16, kernel_size=5)

        self.fc1 = nn.Linear(16 * 4 * 4, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):

        x = F.relu(self.conv1(x))
        x = self.pool(x)

        x = F.relu(self.conv2(x))
        x = self.pool(x)

        x = torch.flatten(x, 1)

        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))

        x = self.fc3(x)

        return x


class MLPDropoutBatchNorm(nn.Module):

    def __init__(self):
        super().__init__()

        self.flatten = nn.Flatten()

        self.fc1 = nn.Linear(28 * 28, 512)
        self.bn1 = nn.BatchNorm1d(512)

        self.fc2 = nn.Linear(512, 128)
        self.bn2 = nn.BatchNorm1d(128)

        self.fc3 = nn.Linear(128, 10)

        self.dropout = nn.Dropout(0.3)

    def forward(self, x):

        x = self.flatten(x)

        x = self.fc1(x)
        x = self.bn1(x)
        x = F.relu(x)
        x = self.dropout(x)

        x = self.fc2(x)
        x = self.bn2(x)
        x = F.relu(x)
        x = self.dropout(x)

        x = self.fc3(x)

        return x


models = {
    "MLP shallow": MLPShallow,
    "MLP deep": MLPDeep,
    "LeNet-5": LeNet5,
    "MLP Dropout + BatchNorm": MLPDropoutBatchNorm
}


def count_parameters(model):

    return sum(
        p.numel()
        for p in model.parameters()
        if p.requires_grad
    )


def train_epoch(model, loader, optimizer, loss_fn):

    model.train()

    total_loss = 0
    correct = 0

    start = time.time()

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

    elapsed = time.time() - start

    loss = total_loss / len(loader.dataset)
    accuracy = correct / len(loader.dataset)

    return loss, accuracy, elapsed


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

    loss = total_loss / len(loader.dataset)
    accuracy = correct / len(loader.dataset)

    return loss, accuracy


def train_model(
    model_class,
    batch_size=64,
    learning_rate=1e-3,
    optimizer_name="Adam",
    epochs=5
):

    train_loader, val_loader, test_loader = create_loaders(
        batch_size
    )

    model = model_class().to(device)

    if optimizer_name == "Adam":

        optimizer = torch.optim.Adam(
            model.parameters(),
            lr=learning_rate
        )

    else:

        optimizer = torch.optim.SGD(
            model.parameters(),
            lr=learning_rate
        )

    loss_fn = nn.CrossEntropyLoss()

    history = []

    for epoch in range(1, epochs + 1):

        train_loss, train_acc, epoch_time = train_epoch(
            model,
            train_loader,
            optimizer,
            loss_fn
        )

        val_loss, val_acc = evaluate(
            model,
            val_loader,
            loss_fn
        )

        history.append({
            "epoch": epoch,
            "train_loss": train_loss,
            "train_acc": train_acc,
            "val_loss": val_loss,
            "val_acc": val_acc,
            "epoch_time": epoch_time
        })

        print(
            f"Epoch {epoch}/{epochs} | "
            f"train_acc={train_acc * 100:.2f}% | "
            f"val_acc={val_acc * 100:.2f}% | "
            f"time={epoch_time:.1f}s"
        )

    test_loss, test_acc = evaluate(
        model,
        test_loader,
        loss_fn
    )

    return model, history, test_acc


comparison_results = []
comparison_histories = {}


print()
print("=" * 70)
print("COMPARAISON DES 4 ARCHITECTURES")
print("=" * 70)


for name, model_class in models.items():

    print()
    print("=" * 70)
    print(name)
    print("=" * 70)

    start = time.time()

    model, history, test_acc = train_model(
        model_class=model_class,
        batch_size=64,
        learning_rate=1e-3,
        optimizer_name="Adam",
        epochs=5
    )

    total_time = time.time() - start

    best_val_acc = max(
        h["val_acc"]
        for h in history
    )

    avg_epoch_time = sum(
        h["epoch_time"]
        for h in history
    ) / len(history)

    parameters = count_parameters(model)

    comparison_results.append({
        "architecture": name,
        "parameters": parameters,
        "best_val_accuracy": best_val_acc,
        "final_test_accuracy": test_acc,
        "avg_time_per_epoch": avg_epoch_time,
        "total_time": total_time
    })

    comparison_histories[name] = history


comparison_df = pd.DataFrame(
    comparison_results
)

comparison_df = comparison_df.sort_values(
    "best_val_accuracy",
    ascending=False
)


print()
print("=" * 70)
print("RÉSULTATS COMPARATIFS")
print("=" * 70)

print(
    comparison_df.round(4).to_string(
        index=False
    )
)


comparison_df.to_csv(
    "comparaison_architectures.csv",
    index=False
)


plt.figure(figsize=(10, 6))

for name, history in comparison_histories.items():

    epochs = [
        h["epoch"]
        for h in history
    ]

    val_acc = [
        h["val_acc"] * 100
        for h in history
    ]

    plt.plot(
        epochs,
        val_acc,
        marker="o",
        label=name
    )

plt.xlabel("Epoch")
plt.ylabel("Validation Accuracy (%)")
plt.title("Comparaison des architectures")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig(
    "courbe_comparaison_architectures.png",
    dpi=150
)

plt.close()


plt.figure(figsize=(10, 6))

plt.bar(
    comparison_df["architecture"],
    comparison_df["best_val_accuracy"] * 100
)

plt.ylabel("Meilleure validation accuracy (%)")
plt.xlabel("Architecture")
plt.title("Validation Accuracy par architecture")
plt.xticks(rotation=25)
plt.tight_layout()

plt.savefig(
    "accuracy_architectures.png",
    dpi=150
)

plt.close()


plt.figure(figsize=(10, 6))

plt.bar(
    comparison_df["architecture"],
    comparison_df["avg_time_per_epoch"]
)

plt.ylabel("Temps moyen par epoch (secondes)")
plt.xlabel("Architecture")
plt.title("Temps moyen par epoch")
plt.xticks(rotation=25)
plt.tight_layout()

plt.savefig(
    "temps_par_epoch.png",
    dpi=150
)

plt.close()


plt.figure(figsize=(10, 6))

plt.bar(
    comparison_df["architecture"],
    comparison_df["parameters"]
)

plt.ylabel("Nombre de paramètres")
plt.xlabel("Architecture")
plt.title("Nombre de paramètres par architecture")
plt.xticks(rotation=25)
plt.tight_layout()

plt.savefig(
    "nombre_parametres.png",
    dpi=150
)

plt.close()


best_architecture = comparison_df.iloc[0]["architecture"]

best_model_class = models[
    best_architecture
]


print()
print("=" * 70)
print("MEILLEURE ARCHITECTURE")
print("=" * 70)

print(
    f"Architecture sélectionnée : {best_architecture}"
)


grid_results = []

batch_sizes = [16, 32, 128]
learning_rates = [1e-2, 1e-3, 1e-4]
optimizers = ["SGD", "Adam"]


grid = list(
    itertools.product(
        batch_sizes,
        learning_rates,
        optimizers
    )
)


print()
print("=" * 70)
print(f"GRID SEARCH : {len(grid)} CONFIGURATIONS")
print("=" * 70)


for number, (
    batch_size,
    learning_rate,
    optimizer_name
) in enumerate(grid, start=1):

    print()
    print(
        f"[{number}/{len(grid)}] "
        f"batch={batch_size} | "
        f"lr={learning_rate} | "
        f"optimizer={optimizer_name}"
    )

    model, history, test_acc = train_model(
        model_class=best_model_class,
        batch_size=batch_size,
        learning_rate=learning_rate,
        optimizer_name=optimizer_name,
        epochs=3
    )

    best_val_acc = max(
        h["val_acc"]
        for h in history
    )

    avg_epoch_time = sum(
        h["epoch_time"]
        for h in history
    ) / len(history)

    grid_results.append({
        "batch_size": batch_size,
        "learning_rate": learning_rate,
        "optimizer": optimizer_name,
        "best_val_accuracy": best_val_acc,
        "test_accuracy": test_acc,
        "avg_time_per_epoch": avg_epoch_time
    })


grid_df = pd.DataFrame(
    grid_results
)

grid_df = grid_df.sort_values(
    "best_val_accuracy",
    ascending=False
)


print()
print("=" * 70)
print("RÉSULTATS DU GRID SEARCH")
print("=" * 70)

print(
    grid_df.round(4).to_string(
        index=False
    )
)


grid_df.to_csv(
    "grid_search_results.csv",
    index=False
)


best_grid = grid_df.iloc[0]


print()
print("=" * 70)
print("MEILLEURE CONFIGURATION DU GRID SEARCH")
print("=" * 70)

print(
    f"Architecture : {best_architecture}"
)

print(
    f"Batch size : {int(best_grid['batch_size'])}"
)

print(
    f"Learning rate : {best_grid['learning_rate']}"
)

print(
    f"Optimizer : {best_grid['optimizer']}"
)

print(
    f"Validation accuracy : "
    f"{best_grid['best_val_accuracy'] * 100:.2f}%"
)

print(
    f"Test accuracy : "
    f"{best_grid['test_accuracy'] * 100:.2f}%"
)


plt.figure(figsize=(10, 6))

labels = [
    f"{int(row.batch_size)} / "
    f"{row.learning_rate} / "
    f"{row.optimizer}"
    for _, row in grid_df.iterrows()
]

values = (
    grid_df["best_val_accuracy"] * 100
)

plt.bar(
    range(len(labels)),
    values
)

plt.ylabel("Validation Accuracy (%)")
plt.xlabel("Configuration")
plt.title("Résultats du Grid Search")
plt.xticks(
    range(len(labels)),
    labels,
    rotation=90
)

plt.tight_layout()

plt.savefig(
    "grid_search_accuracy.png",
    dpi=150
)

plt.close()


best_arch_row = comparison_df.iloc[0]

best_arch_acc = (
    best_arch_row["best_val_accuracy"] * 100
)

best_arch_params = (
    int(best_arch_row["parameters"])
)

best_arch_time = (
    best_arch_row["avg_time_per_epoch"]
)

best_grid_acc = (
    best_grid["best_val_accuracy"] * 100
)

best_grid_test = (
    best_grid["test_accuracy"] * 100
)


conclusion = f"""
CONCLUSION — COMPARATIF ARCHITECTURES ET HYPERPARAMÈTRES

Le dataset MNIST a été utilisé pour comparer quatre architectures :
MLP shallow, MLP deep, LeNet-5 et MLP avec Dropout + BatchNorm.

L'architecture ayant obtenu la meilleure validation accuracy lors de la
comparaison est : {best_architecture}.

Sa meilleure validation accuracy est de {best_arch_acc:.2f}%.
Elle possède {best_arch_params:,} paramètres et son temps moyen par epoch
est de {best_arch_time:.2f} secondes.

Un grid search a ensuite été réalisé sur cette architecture avec :
- batch size : 16, 32 et 128 ;
- learning rate : 1e-2, 1e-3 et 1e-4 ;
- optimizers : SGD et Adam.

Cela représente 18 configurations.

La meilleure configuration trouvée est :
- batch size : {int(best_grid["batch_size"])};
- learning rate : {best_grid["learning_rate"]};
- optimizer : {best_grid["optimizer"]}.

Cette configuration obtient une validation accuracy de
{best_grid_acc:.2f}% et une test accuracy de {best_grid_test:.2f}%.

Cette expérience montre que les performances dépendent à la fois de
l'architecture et des hyperparamètres. Le nombre de paramètres ne suffit
pas à déterminer les performances : il faut également considérer la
précision obtenue et le temps d'entraînement.

Le learning rate influence directement la vitesse et la stabilité de
l'apprentissage. Le batch size influence le nombre de mises à jour et le
temps nécessaire pour parcourir le dataset. Le choix de l'optimizer
influence également la convergence.

Les résultats obtenus sont spécifiques à cette exécution et peuvent
varier légèrement selon le matériel et l'initialisation du modèle.
"""


with open(
    "conclusion.txt",
    "w",
    encoding="utf-8"
) as f:

    f.write(conclusion)


print()
print("=" * 70)
print("FICHIERS CRÉÉS")
print("=" * 70)

print("comparaison_architectures.csv")
print("grid_search_results.csv")
print("courbe_comparaison_architectures.png")
print("accuracy_architectures.png")
print("temps_par_epoch.png")
print("nombre_parametres.png")
print("grid_search_accuracy.png")
print("conclusion.txt")

print()
print("Étude terminée.")