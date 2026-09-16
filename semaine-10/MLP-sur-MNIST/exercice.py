import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay


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


train_loader = DataLoader(
    train_ds,
    batch_size=64,
    shuffle=True
)

test_loader = DataLoader(
    test_ds,
    batch_size=64,
    shuffle=False
)


class MLP(nn.Module):

    def __init__(self):
        super().__init__()

        self.flatten = nn.Flatten()

        self.fc1 = nn.Linear(28 * 28, 512)
        self.fc2 = nn.Linear(512, 128)
        self.fc3 = nn.Linear(128, 10)

    def forward(self, x):

        x = self.flatten(x)

        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))

        return self.fc3(x)


model = MLP().to(device)

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=1e-3
)

loss_fn = nn.CrossEntropyLoss()


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

    loss = total_loss / len(loader.dataset)
    accuracy = correct / len(loader.dataset)

    return loss, accuracy


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


for epoch in range(1, 11):

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
        f"Epoch {epoch:2d}/10 | "
        f"train_loss={train_loss:.4f} | "
        f"train_acc={train_acc * 100:.2f}% | "
        f"test_loss={test_loss:.4f} | "
        f"test_acc={test_acc * 100:.2f}%"
    )


print()
print("=" * 60)
print(f"Test accuracy finale : {test_acc * 100:.2f}%")

if test_acc > 0.97:
    print("Objectif atteint : test accuracy > 97%")
else:
    print("Objectif non atteint : test accuracy <= 97%")


model.eval()

all_predictions = []
all_labels = []

with torch.no_grad():

    for x, y in test_loader:

        x = x.to(device)

        logits = model(x)

        predictions = logits.argmax(dim=1)

        all_predictions.extend(
            predictions.cpu().numpy()
        )

        all_labels.extend(
            y.numpy()
        )


cm = confusion_matrix(
    all_labels,
    all_predictions
)

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=list(range(10))
)

fig, ax = plt.subplots(figsize=(9, 9))

disp.plot(
    ax=ax,
    cmap="Blues",
    values_format="d"
)

plt.title("Matrice de confusion - MNIST")
plt.tight_layout()
plt.show()


wrong_indices = []

for i in range(len(test_ds)):

    x, y = test_ds[i]

    with torch.no_grad():

        logits = model(
            x.unsqueeze(0).to(device)
        )

        prediction = logits.argmax(
            dim=1
        ).item()

    if prediction != y:

        wrong_indices.append(
            (i, prediction, y)
        )

    if len(wrong_indices) == 5:
        break


fig, axes = plt.subplots(
    1,
    5,
    figsize=(15, 3)
)

for ax, (index, prediction, real_label) in zip(
    axes,
    wrong_indices
):

    x, y = test_ds[index]

    ax.imshow(
        x.squeeze(),
        cmap="gray"
    )

    ax.set_title(
        f"Vrai : {real_label}\nPrédit : {prediction}"
    )

    ax.axis("off")

plt.suptitle("5 images mal classées")
plt.tight_layout()
plt.show()