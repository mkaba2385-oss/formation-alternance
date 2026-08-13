import logging

logger = logging.getLogger(__name__)


def addition(a: int, b: int) -> int:
    logger.info("Calcul en cours...")
    # TODO(moussa): optimiser cette fonction si besoin
    return a + b


def test_addition() -> None:
    assert addition(2, 2) == 4
