import logging
from collections.abc import Callable
from functools import wraps
from typing import cast

logger = logging.getLogger(__name__)


def log_calls[**P, R](func: Callable[P, R]) -> Callable[P, R]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        logger.info("Appel de la fonction %s", func.__name__)
        return func(*args, **kwargs)

    return cast(Callable[P, R], wrapper)
