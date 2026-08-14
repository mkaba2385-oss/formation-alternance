import pytest

from biblio.service import BibliothequeService


def test_ajouter_livre(service: BibliothequeService) -> None:
    livre = service.ajouter_livre(
        "1984",
        "George Orwell",
        1949,
    )

    assert livre.id == 1
    assert livre.titre == "1984"
    assert livre.disponible is True


def test_ajouter_plusieurs_livres(service: BibliothequeService) -> None:
    livre1 = service.ajouter_livre("1984", "George Orwell", 1949)
    livre2 = service.ajouter_livre("Le Petit Prince", "Saint-Exupéry", 1943)

    assert livre1.id == 1
    assert livre2.id == 2


def test_chercher_livre(service: BibliothequeService) -> None:
    service.ajouter_livre("1984", "George Orwell", 1949)

    livre = service.chercher_livre(1)

    assert livre is not None
    assert livre.titre == "1984"


def test_supprimer_livre(service: BibliothequeService) -> None:
    service.ajouter_livre("1984", "George Orwell", 1949)

    assert service.supprimer_livre(1) is True
    assert service.chercher_livre(1) is None


def test_supprimer_livre_inexistant(service: BibliothequeService) -> None:
    assert service.supprimer_livre(999) is False


def test_emprunter_livre(service: BibliothequeService) -> None:
    service.ajouter_livre("1984", "George Orwell", 1949)

    emprunt = service.emprunter_livre(1, "Moussa")

    assert emprunt.livre_id == 1
    assert emprunt.emprunteur == "Moussa"

    livre = service.chercher_livre(1)

    assert livre is not None
    assert livre.disponible is False


def test_emprunter_livre_inexistant(service: BibliothequeService) -> None:
    with pytest.raises(ValueError, match="Livre introuvable"):
        service.emprunter_livre(999, "Moussa")


def test_emprunter_livre_deja_emprunte(service: BibliothequeService) -> None:
    service.ajouter_livre("1984", "George Orwell", 1949)

    service.emprunter_livre(1, "Moussa")

    with pytest.raises(ValueError, match="déjà emprunté"):
        service.emprunter_livre(1, "Ali")


def test_rendre_livre(service: BibliothequeService) -> None:
    service.ajouter_livre("1984", "George Orwell", 1949)

    service.emprunter_livre(1, "Moussa")
    resultat = service.rendre_livre(1)

    assert resultat is True

    livre = service.chercher_livre(1)

    assert livre is not None
    assert livre.disponible is True


def test_rendre_livre_inexistant(service: BibliothequeService) -> None:
    with pytest.raises(ValueError, match="Livre introuvable"):
        service.rendre_livre(999)


def test_rendre_livre_deja_disponible(service: BibliothequeService) -> None:
    service.ajouter_livre("1984", "George Orwell", 1949)

    with pytest.raises(ValueError, match="pas emprunté"):
        service.rendre_livre(1)
