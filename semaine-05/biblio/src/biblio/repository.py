import json
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

from .models import Livre


@contextmanager
def bibliotheque_ouverte(
    chemin: Path,
) -> Generator[list[dict[str, object]], None, None]:
    if chemin.exists():
        with open(chemin, encoding="utf-8") as fichier:
            donnees = json.load(fichier)
    else:
        donnees = []

    yield donnees

    with open(chemin, "w", encoding="utf-8") as fichier:
        json.dump(donnees, fichier, indent=2, ensure_ascii=False)


class LivreRepository:
    def __init__(self, chemin: Path):
        self.chemin = chemin

    def tous(self) -> list[Livre]:
        with bibliotheque_ouverte(self.chemin) as donnees:
            return [Livre.model_validate(d) for d in donnees]

    def ajouter(self, livre: Livre) -> None:
        with bibliotheque_ouverte(self.chemin) as donnees:
            donnees.append(livre.model_dump())

    def trouver(self, livre_id: int) -> Livre | None:
        livres = self.tous()

        for livre in livres:
            if livre.id == livre_id:
                return livre

        return None

    def supprimer(self, livre_id: int) -> bool:
        with bibliotheque_ouverte(self.chemin) as donnees:
            for i, donnees_livre in enumerate(donnees):
                if donnees_livre.get("id") == livre_id:
                    donnees.pop(i)
                    return True

        return False

    def mettre_a_jour(self, livre: Livre) -> bool:
        with bibliotheque_ouverte(self.chemin) as donnees:
            for i, donnees_livre in enumerate(donnees):
                if donnees_livre.get("id") == livre.id:
                    donnees[i] = livre.model_dump()
                    return True

        return False
