from typing import List, Optional, Tuple

Coord = Tuple[int, int]


def trouver_depart_et_sortie(grille: List[List[str]]) -> Tuple[Optional[Coord], Optional[Coord]]:
    """Recherche les positions de S et E."""
    depart = None
    sortie = None

    for i in range(len(grille)):
        for j in range(len(grille[i])):
            if grille[i][j] == "S":
                depart = (i, j)
            elif grille[i][j] == "E":
                sortie = (i, j)

    return depart, sortie


def resoudre_labyrinthe(grille: List[List[str]]) -> Optional[List[Coord]]:
    """Retourne un chemin de S à E ou None."""

    # Cas grille vide
    if not grille or not grille[0]:
        return None

    depart, sortie = trouver_depart_et_sortie(grille)

    # Cas sans départ ou sans sortie
    if depart is None or sortie is None:
        return None

    # Cas où le départ est la sortie
    if depart == sortie:
        return [depart]

    visites = set()

    def explorer(position: Coord) -> Optional[List[Coord]]:
        x, y = position

        # Hors limites
        if x < 0 or x >= len(grille):
            return None
        if y < 0 or y >= len(grille[0]):
            return None

        # Déjà visité
        if position in visites:
            return None

        # Mur
        if grille[x][y] == "#":
            return None

        # Sortie trouvée
        if position == sortie:
            return [position]

        visites.add(position)

        directions = [
            (-1, 0),   # haut
            (1, 0),    # bas
            (0, -1),   # gauche
            (0, 1),    # droite
        ]

        for dx, dy in directions:
            chemin = explorer((x + dx, y + dy))
            if chemin is not None:
                return [position] + chemin

        return None

    return explorer(depart)


def afficher_solution(grille: List[List[str]], chemin: Optional[List[Coord]]) -> None:
    """Affiche le labyrinthe avec le chemin."""

    copie = [ligne[:] for ligne in grille]

    if chemin:
        for x, y in chemin:
            if copie[x][y] == " ":
                copie[x][y] = "."

    for ligne in copie:
        print("".join(ligne))


# Exemple de labyrinthe

labyrinthe = [
    list("##########"),
    list("#S     # #"),
    list("### ## # #"),
    list("#   ##   #"),
    list("# ###### #"),
    list("#      E #"),
    list("##########"),
]

chemin = resoudre_labyrinthe(labyrinthe)

if chemin is None:
    print("Aucun chemin trouvé.")
else:
    print("Chemin trouvé :")
    print(chemin)
    print()
    afficher_solution(labyrinthe, chemin)