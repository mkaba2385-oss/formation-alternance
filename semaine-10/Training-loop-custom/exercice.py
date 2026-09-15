from __future__ import annotations

import random
from dataclasses import dataclass, asdict
from pathlib import Path

import numpy as np
import torch
from torch import nn
from torch.utils.data import Dataset, DataLoader, random_split
from torch.utils.tensorboard import SummaryWriter


@dataclass
class Config:
    seed: int = 42
    n_samples: int = 1200
    val_ratio: float = 0.20
    batch_size: int = 32
    accumulation_steps: int = 4
    epochs: int = 80
    learning_rate: float = 1e-2
    weight_decay: float = 1e-4
    clip_grad_norm: float = 1.0
    patience: int = 10
    min_delta: float = 1e-4
    num_workers: int = 0
    log_dir: str = "runs/training_loop_custom"
    checkpoint_dir: str = "checkpoints"


CFG = Config()


def seed_everything(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


seed_everything(CFG.seed)

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print(f"Device utilisé : {DEVICE}")


class ToyRegressionDataset(Dataset):

    def __init__(
        self,
        n_samples: int,
        seed: int = 42,
    ) -> None:

        generator = torch.Generator().manual_seed(seed)

        self.x = torch.randn(
            n_samples,
            3,
            generator=generator,
        )

        noise = 0.15 * torch.randn(
            n_samples,
            1,
            generator=generator,
        )

        self.y = (
            3.0 * self.x[:, 0:1]
            - 2.0 * self.x[:, 1:2]
            + 0.5 * self.x[:, 2:3].pow(2)
            + noise
        )

    def __len__(self) -> int:
        return len(self.x)

    def __getitem__(
        self,
        index: int,
    ) -> dict[str, torch.Tensor]:

        return {
            "features": self.x[index],
            "target": self.y[index],
        }


def custom_collate(
    batch: list[dict[str, torch.Tensor]],
) -> dict[str, torch.Tensor]:

    return {
        "features": torch.stack(
            [item["features"] for item in batch]
        ),
        "target": torch.stack(
            [item["target"] for item in batch]
        ),
    }


print("1. Création du dataset")

dataset = ToyRegressionDataset(
    n_samples=CFG.n_samples,
    seed=CFG.seed,
)

print("2. Split du dataset")

val_size = int(
    len(dataset) * CFG.val_ratio
)

train_size = len(dataset) - val_size

split_generator = torch.Generator().manual_seed(
    CFG.seed
)

train_dataset, val_dataset = random_split(
    dataset,
    [train_size, val_size],
    generator=split_generator,
)

print("3. Création du DataLoader train")

train_loader = DataLoader(
    train_dataset,
    batch_size=CFG.batch_size,
    shuffle=True,
    num_workers=CFG.num_workers,
    pin_memory=torch.cuda.is_available(),
    collate_fn=custom_collate,
)

print("4. Création du DataLoader validation")

val_loader = DataLoader(
    val_dataset,
    batch_size=CFG.batch_size,
    shuffle=False,
    num_workers=CFG.num_workers,
    pin_memory=torch.cuda.is_available(),
    collate_fn=custom_collate,
)


class MLPRegressor(nn.Module):

    def __init__(self) -> None:
        super().__init__()

        self.network = nn.Sequential(
            nn.Linear(3, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
        )

    def forward(
        self,
        x: torch.Tensor,
    ) -> torch.Tensor:

        return self.network(x)


print("5. Création du modèle")

model = MLPRegressor().to(DEVICE)

print("6. Création de la fonction de perte")

criterion = nn.MSELoss()

print("7. Création de l'optimiseur")

optimizer = torch.optim.SGD(
    model.parameters(),
    lr=CFG.learning_rate,
    momentum=0.9,
    weight_decay=CFG.weight_decay,
)

print("8. Création du scheduler")

scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
    optimizer,
    mode="min",
    factor=0.5,
    patience=3,
    min_lr=1e-6,
)

print("9. Création de TensorBoard")

writer = SummaryWriter(
    log_dir=CFG.log_dir
)

print("10. Configuration TensorBoard")

writer.add_text(
    "Configuration",
    str(asdict(CFG)),
    0,
)

checkpoint_dir = Path(
    CFG.checkpoint_dir
)

checkpoint_dir.mkdir(
    parents=True,
    exist_ok=True,
)

best_checkpoint = (
    checkpoint_dir / "best_model.pt"
)

print("11. Initialisation terminée")


def train_one_epoch(
    model: nn.Module,
    loader: DataLoader,
    optimizer: torch.optim.Optimizer,
    criterion: nn.Module,
    device: torch.device,
    accumulation_steps: int,
    clip_grad_norm: float,
) -> float:

    model.train()

    optimizer.zero_grad(
        set_to_none=True
    )

    running_loss = 0.0
    total_samples = 0

    for step, batch in enumerate(loader):

        features = batch["features"].to(
            device,
            non_blocking=True,
        )

        targets = batch["target"].to(
            device,
            non_blocking=True,
        )

        predictions = model(features)

        loss = criterion(
            predictions,
            targets,
        )

        loss_for_backward = (
            loss / accumulation_steps
        )

        loss_for_backward.backward()

        accumulation_boundary = (
            (step + 1) % accumulation_steps == 0
            or (step + 1) == len(loader)
        )

        if accumulation_boundary:

            torch.nn.utils.clip_grad_norm_(
                model.parameters(),
                max_norm=clip_grad_norm,
            )

            optimizer.step()

            optimizer.zero_grad(
                set_to_none=True
            )

        batch_size = features.size(0)

        running_loss += (
            loss.detach().item()
            * batch_size
        )

        total_samples += batch_size

    return running_loss / total_samples


@torch.no_grad()
def validate(
    model: nn.Module,
    loader: DataLoader,
    criterion: nn.Module,
    device: torch.device,
) -> float:

    model.eval()

    running_loss = 0.0
    total_samples = 0

    for batch in loader:

        features = batch["features"].to(
            device,
            non_blocking=True,
        )

        targets = batch["target"].to(
            device,
            non_blocking=True,
        )

        predictions = model(features)

        loss = criterion(
            predictions,
            targets,
        )

        batch_size = features.size(0)

        running_loss += (
            loss.item()
            * batch_size
        )

        total_samples += batch_size

    return running_loss / total_samples


def save_checkpoint(
    path: Path,
    epoch: int,
    model: nn.Module,
    optimizer: torch.optim.Optimizer,
    scheduler: torch.optim.lr_scheduler.ReduceLROnPlateau,
    val_loss: float,
) -> None:

    torch.save(
        {
            "epoch": epoch,
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "scheduler_state_dict": scheduler.state_dict(),
            "val_loss": val_loss,
            "config": asdict(CFG),
        },
        path,
    )


best_val_loss = float("inf")

epochs_without_improvement = 0

history = {
    "train_loss": [],
    "val_loss": [],
    "learning_rate": [],
}


print("12. Début de l'entraînement")


for epoch in range(
    1,
    CFG.epochs + 1,
):

    train_loss = train_one_epoch(
        model=model,
        loader=train_loader,
        optimizer=optimizer,
        criterion=criterion,
        device=DEVICE,
        accumulation_steps=CFG.accumulation_steps,
        clip_grad_norm=CFG.clip_grad_norm,
    )

    val_loss = validate(
        model=model,
        loader=val_loader,
        criterion=criterion,
        device=DEVICE,
    )

    scheduler.step(val_loss)

    current_lr = (
        optimizer.param_groups[0]["lr"]
    )

    history["train_loss"].append(
        train_loss
    )

    history["val_loss"].append(
        val_loss
    )

    history["learning_rate"].append(
        current_lr
    )

    writer.add_scalar(
        "Loss/train",
        train_loss,
        epoch,
    )

    writer.add_scalar(
        "Loss/validation",
        val_loss,
        epoch,
    )

    writer.add_scalar(
        "Learning_rate",
        current_lr,
        epoch,
    )

    print(
        f"Epoch {epoch:03d}/{CFG.epochs} | "
        f"train_loss={train_loss:.6f} | "
        f"val_loss={val_loss:.6f} | "
        f"lr={current_lr:.2e}"
    )

    if val_loss < best_val_loss - CFG.min_delta:

        best_val_loss = val_loss

        epochs_without_improvement = 0

        save_checkpoint(
            path=best_checkpoint,
            epoch=epoch,
            model=model,
            optimizer=optimizer,
            scheduler=scheduler,
            val_loss=val_loss,
        )

        print(
            f"Best model sauvegardé : "
            f"{best_checkpoint}"
        )

    else:

        epochs_without_improvement += 1

        print(
            f"Pas d'amélioration : "
            f"{epochs_without_improvement}/"
            f"{CFG.patience}"
        )

        if epochs_without_improvement >= CFG.patience:

            print(
                "Early stopping déclenché."
            )

            break


print("13. Chargement du meilleur modèle")

checkpoint = torch.load(
    best_checkpoint,
    map_location=DEVICE,
    weights_only=False,
)

model.load_state_dict(
    checkpoint["model_state_dict"]
)

print(
    "\nEntraînement terminé."
)

print(
    f"Meilleur epoch : "
    f"{checkpoint['epoch']}"
)

print(
    f"Meilleure val_loss : "
    f"{checkpoint['val_loss']:.6f}"
)

print(
    f"Checkpoint : "
    f"{best_checkpoint}"
)

writer.flush()
writer.close()

print(
    f"\nTensorBoard : "
    f"tensorboard --logdir {CFG.log_dir}"
)