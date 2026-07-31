import time


def chunk(sequence, size):
    """
    Découpe une liste en sous-listes de taille 'size'.
    """
    return [
        sequence[i:i + size]
        for i in range(0, len(sequence), size)
    ]


def retry(function, retries=3, delay=1):
    """
    Exécute une fonction en réessayant en cas d'exception.
    """
    for attempt in range(retries):
        try:
            return function()
        except Exception:
            if attempt == retries - 1:
                raise
            time.sleep(delay)


def format_fcfa(amount):
    """
    Formate un montant en FCFA.
    """
    return f"{amount:,.0f} FCFA".replace(",", " ")