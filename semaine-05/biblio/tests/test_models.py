import pytest
from pydantic import ValidationError

from biblio.models import Livre


def test_creation_livre() -> None:
    livre = Livre(
        id=1,
        titre="1984",
        auteur="George Orwell",
        annee=1949,
    )

    assert livre.titre == "1984"
    assert livre.auteur == "George Orwell"
    assert livre.disponible is True


@pytest.mark.parametrize(
    "titre,auteur",
    [
        ("", "Orwell"),
        ("1984", ""),
    ],
)
def test_livre_invalide(titre: str, auteur: str) -> None:
    with pytest.raises(ValidationError):
        Livre(
            id=1,
            titre=titre,
            auteur=auteur,
            annee=1949,
        )


def test_annee_invalide() -> None:
    with pytest.raises(ValidationError):
        Livre(
            id=1,
            titre="1984",
            auteur="Orwell",
            annee=500,
        )
