# Exercice 1 - Somme des chiffres

def somme_chiffres_iter(n):
    somme = 0
    while n > 0:
        somme += n % 10
        n //= 10
    return somme


# Test
print(somme_chiffres_iter(1234))


# Exercice 2 - PGCD

def pgcd_iter(a, b):
    while b != 0:
        a, b = b, a % b
    return a


print(pgcd_iter(48, 18))


# Exercice 3 - Tri fusion

def fusionner(gauche, droite):
    resultat = []
    i = j = 0

    while i < len(gauche) and j < len(droite):
        if gauche[i] <= droite[j]:
            resultat.append(gauche[i])
            i += 1
        else:
            resultat.append(droite[j])
            j += 1

    resultat.extend(gauche[i:])
    resultat.extend(droite[j:])
    return resultat


def merge_sort_iter(liste):
    largeur = 1
    n = len(liste)

    while largeur < n:
        resultat = []

        for i in range(0, n, 2 * largeur):
            gauche = liste[i:i + largeur]
            droite = liste[i + largeur:i + 2 * largeur]
            resultat.extend(fusionner(gauche, droite))

        liste = resultat
        largeur *= 2

    return liste


print(merge_sort_iter([3, 1, 4, 1, 5, 9, 2, 6]))