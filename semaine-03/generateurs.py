from contextlib import contextmanager
from itertools import islice
import itertools
import time


# 1. Générateur infini de nombres premiers
# (Crible d'Eratosthène adapté)

def premiers():
    nombres = {}
    n = 2

    while True:
        if n not in nombres:
            yield n
            nombres[n * n] = [n]
        else:
            for p in nombres[n]:
                nombres.setdefault(p + n, []).append(p)
            del nombres[n]
        n += 1


print("10 premiers nombres premiers :")
print(list(islice(premiers(), 10)))


# 2. Context manager pour mesurer le temps

@contextmanager
def mesurer_temps(message="Temps d'exécution"):
    debut = time.perf_counter()
    try:
        yield
    finally:
        fin = time.perf_counter()
        print(f"{message} : {fin - debut:.6f} secondes")


with mesurer_temps("Calcul des 100000 premiers carrés"):
    total = sum(i * i for i in range(100000))


# 3. Fonction chunk() lazy


def chunk(iterable, taille):
    it = iter(iterable)

    while True:
        morceau = list(itertools.islice(it, taille))
        if not morceau:
            break
        yield morceau


print("\nDécoupage :")

for morceau in chunk(range(20), 6):
    print(morceau)


# 4. Test sur un très gros fichier

def lire_gros_fichier(nom_fichier):
    with open(nom_fichier, encoding="utf-8") as fichier:
        for ligne in fichier:
            yield ligne.rstrip()


print("\nExemple de lecture lazy :")
