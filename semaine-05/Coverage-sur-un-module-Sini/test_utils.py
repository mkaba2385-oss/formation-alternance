import logging
from utils import timer


def test_timer_renvoie_resultat_fonction():
    @timer
    def addition(a: int, b: int) -> int:
        return a + b

    resultat = addition(2, 3)
    assert resultat == 5


def test_timer_conserve_metadonnees_fonction():
    @timer
    def ma_fonction():
        """Docstring de test."""
        pass

    assert ma_fonction.__name__ == "ma_fonction"
    assert ma_fonction.__doc__ == "Docstring de test."


def test_timer_log_temps_execution(caplog):
    caplog.set_level(logging.DEBUG, logger="sini.services")

    @timer
    def fonction_lente():
        return "ok"

    res = fonction_lente()

    assert res == "ok"
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == "DEBUG"
    assert "[PERF] fonction_lente a pris" in caplog.records[0].message


def test_timer_transmet_args_et_kwargs():
    @timer
    def fonction_avec_arguments(*args, **kwargs):
        return sum(args) + kwargs.get("bonus", 0)

    assert fonction_avec_arguments(1, 2, 3, bonus=4) == 10