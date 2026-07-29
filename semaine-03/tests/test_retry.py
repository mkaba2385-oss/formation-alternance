from retry import retry


# premier test réussite après plusieurs essais
def test_retry_success():

    compteur = {"n" : 0}

    @retry(max_attempts=5, delay =0)
    def fonction():

        compteur["n"] += 1

        if compteur["n"] < 3:
            raise ValueError("erreur")
        return "ok"

    assert fonction() == "ok"
    assert compteur["n"] == 3

# second test échec définitif

import pytest
from retry import retry


def test_retry_failure():

    compteur = {"n": 0}

    @retry(max_attempts=3, delay=0)
    def fonction():
        compteur["n"] += 1
        raise ValueError("Toujours en erreur")

    with pytest.raises(ValueError):
        fonction()

    assert compteur["n"] == 3


# test 3 exception non concernée
import pytest
from retry import retry


def test_retry_wrong_exception():

    compteur = {"n": 0}

    @retry(
        max_attempts=5,
        delay=0,
        exceptions=(ValueError,)
    )
    def fonction():

        compteur["n"] += 1
        raise TypeError("Mauvaise exception")

    with pytest.raises(TypeError):
        fonction()

    
    assert compteur["n"] == 1