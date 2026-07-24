import timeit


def ma_fonction1(n):
    """Vérifie si n est divisible par 7.

    Complexité temporelle : O(n) - Complexité linéaire.
    La boucle parcourt n éléments. Plus n est grand, plus le nombre
    d'opérations augmente proportionnellement.
    """
    divis = False
    for i in range(n):
        if i * 7 == n:
            divis = True
    return divis


def ma_fonction2(n):
    """Vérifie si n est divisible par 7.

    Complexité temporelle : O(1) - Complexité constante.
    L'opération modulo (%) s'exécute en un nombre constant d'instructions
    processeur, indépendamment de la taille de n.
    """
    if n % 7 == 0:
        return True
    else:
        return False


# --- Optimisation et mesure avec timeit ---


def ma_fonction1_optimisee(n):
    """Version optimisée de ma_fonction1.

    Complexité temporelle : O(1) - Complexité constante.
    On remplace la recherche par boucle O(n) par un calcul direct.
    """
    return n % 7 == 0


if __name__ == "__main__":
    n = 10000

    # Mesure sur 1 000 exécutions pour obtenir une moyenne fiable
    temps_f1 = timeit.timeit(lambda: ma_fonction1(n), number=1000)
    temps_f2 = timeit.timeit(lambda: ma_fonction2(n), number=1000)
    temps_f1_opti = timeit.timeit(
        lambda: ma_fonction1_optimisee(n), number=1000
    )

    print(f"--- RÉSULTATS DES MESURES (n = {n}, 1000 exécutions) ---")
    print(f"ma_fonction1 (O(n))          : {temps_f1:.6f} secondes")
    print(f"ma_fonction2 (O(1))          : {temps_f2:.6f} secondes")
    print(f"ma_fonction1_optimisee (O(1)): {temps_f1_opti:.6f} secondes")