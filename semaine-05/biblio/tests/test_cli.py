from pathlib import Path

from pytest import CaptureFixture, MonkeyPatch

from biblio.cli import main


def test_ajouter_et_lister(
    capsys: CaptureFixture[str], tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)

    main(["ajouter", "1984", "George Orwell", "1949"])

    sortie = capsys.readouterr()
    assert "Livre ajouté : 1 - 1984" in sortie.out

    main(["lister"])

    sortie = capsys.readouterr()
    assert "1984" in sortie.out
    assert "George Orwell" in sortie.out


def test_chercher_livre(
    capsys: CaptureFixture[str], tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)

    main(["ajouter", "1984", "George Orwell", "1949"])
    capsys.readouterr()

    main(["chercher", "1"])

    sortie = capsys.readouterr()
    assert "1984" in sortie.out


def test_chercher_livre_inexistant(
    capsys: CaptureFixture[str],
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)

    main(["chercher", "999"])

    sortie = capsys.readouterr()
    assert "Livre introuvable." in sortie.out


def test_supprimer_livre(
    capsys: CaptureFixture[str], tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)

    main(["ajouter", "1984", "George Orwell", "1949"])
    capsys.readouterr()

    main(["supprimer", "1"])

    sortie = capsys.readouterr()
    assert "Livre supprimé." in sortie.out


def test_emprunter_et_rendre(
    capsys: CaptureFixture[str], tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)

    main(["ajouter", "1984", "George Orwell", "1949"])
    capsys.readouterr()

    main(["emprunter", "1", "Moussa"])

    sortie = capsys.readouterr()
    assert "Livre emprunté par Moussa" in sortie.out

    main(["rendre", "1"])

    sortie = capsys.readouterr()
    assert "Livre rendu." in sortie.out
