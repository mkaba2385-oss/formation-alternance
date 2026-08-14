from pathlib import Path

from biblio.models import Livre
from biblio.repository import LivreRepository


def test_ajouter_et_lister(tmp_path: Path) -> None:
    chemin = tmp_path / "bibliotheque.json"
    repository = LivreRepository(chemin)

    livre = Livre(
        id=1,
        titre="1984",
        auteur="George Orwell",
        annee=1949,
    )

    repository.ajouter(livre)

    livres = repository.tous()

    assert len(livres) == 1
    assert livres[0].titre == "1984"


def test_trouver_livre(tmp_path: Path) -> None:
    chemin = tmp_path / "bibliotheque.json"
    repository = LivreRepository(chemin)

    livre = Livre(
        id=1,
        titre="1984",
        auteur="George Orwell",
        annee=1949,
    )

    repository.ajouter(livre)

    resultat = repository.trouver(1)

    assert resultat is not None
    assert resultat.titre == "1984"


def test_trouver_livre_inexistant(tmp_path: Path) -> None:
    chemin = tmp_path / "bibliotheque.json"
    repository = LivreRepository(chemin)

    assert repository.trouver(999) is None


def test_supprimer_livre(tmp_path: Path) -> None:
    chemin = tmp_path / "bibliotheque.json"
    repository = LivreRepository(chemin)

    livre = Livre(
        id=1,
        titre="1984",
        auteur="George Orwell",
        annee=1949,
    )

    repository.ajouter(livre)

    assert repository.supprimer(1) is True
    assert repository.tous() == []


def test_supprimer_livre_inexistant(tmp_path: Path) -> None:
    chemin = tmp_path / "bibliotheque.json"
    repository = LivreRepository(chemin)

    assert repository.supprimer(999) is False


def test_mettre_a_jour_livre(tmp_path: Path) -> None:
    chemin = tmp_path / "bibliotheque.json"
    repository = LivreRepository(chemin)

    livre = Livre(
        id=1,
        titre="1984",
        auteur="George Orwell",
        annee=1949,
    )

    repository.ajouter(livre)

    livre.disponible = False

    assert repository.mettre_a_jour(livre) is True

    resultat = repository.trouver(1)

    assert resultat is not None
    assert resultat.disponible is False
