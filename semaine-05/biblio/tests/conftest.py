from collections.abc import Generator
from pathlib import Path

import pytest

from biblio.repository import LivreRepository
from biblio.service import BibliothequeService


@pytest.fixture
def service(tmp_path: Path) -> Generator[BibliothequeService, None, None]:
    chemin = tmp_path / "bibliotheque.json"
    repository = LivreRepository(chemin)
    yield BibliothequeService(repository)
