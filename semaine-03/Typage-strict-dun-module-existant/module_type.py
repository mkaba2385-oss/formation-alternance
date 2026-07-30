from typing import TypedDict


class Livre(TypedDict):
    id: int
    titre: str
    auteur: str
    annee: int
    disponible: bool


class Bibliotheque:
    def __init__(self) -> None:
        self.livres: list[Livre] = []

    def ajouter_livre(
        self,
        id: int,
        titre: str,
        auteur: str,
        annee: int
    ) -> None:
        livre: Livre = {
            "id": id,
            "titre": titre,
            "auteur": auteur,
            "annee": annee,
            "disponible": True,
        }
        self.livres.append(livre)

    def afficher_livres(self) -> None:
        for livre in self.livres:
            print(
                f"{livre['id']} - "
                f"{livre['titre']} - "
                f"{livre['auteur']} - "
                f"{livre['annee']} - "
                f"{livre['disponible']}"
            )

    def chercher_par_id(self, id: int) -> Livre | None:
        for livre in self.livres:
            if livre["id"] == id:
                return livre
        return None

    def chercher_par_titre(self, titre: str) -> list[Livre]:
        resultat: list[Livre] = []

        for livre in self.livres:
            if titre.lower() in livre["titre"].lower():
                resultat.append(livre)

        return resultat

    def emprunter(self, id: int) -> bool:
        livre = self.chercher_par_id(id)

        if livre is None:
            return False

        if not livre["disponible"]:
            return False

        livre["disponible"] = False
        return True

    def rendre(self, id: int) -> bool:
        livre = self.chercher_par_id(id)

        if livre is None:
            return False

        livre["disponible"] = True
        return True

    def supprimer(self, id: int) -> bool:
        livre = self.chercher_par_id(id)

        if livre is None:
            return False

        self.livres.remove(livre)
        return True

    def nombre_livres(self) -> int:
        return len(self.livres)

    def nombre_disponibles(self) -> int:
        compteur: int = 0

        for livre in self.livres:
            if livre["disponible"]:
                compteur += 1

        return compteur

    def livres_par_auteur(self, auteur: str) -> list[Livre]:
        resultat: list[Livre] = []

        for livre in self.livres:
            if livre["auteur"].lower() == auteur.lower():
                resultat.append(livre)

        return resultat

    def livres_apres(self, annee: int) -> list[Livre]:
        resultat: list[Livre] = []

        for livre in self.livres:
            if livre["annee"] >= annee:
                resultat.append(livre)

        return resultat


def creer_bibliotheque() -> Bibliotheque:
    biblio = Bibliotheque()

    biblio.ajouter_livre(
        1,
        "Le Petit Prince",
        "Antoine de Saint-Exupéry",
        1943,
    )

    biblio.ajouter_livre(
        2,
        "L'Étranger",
        "Albert Camus",
        1942,
    )

    biblio.ajouter_livre(
        3,
        "Les Misérables",
        "Victor Hugo",
        1862,
    )

    biblio.ajouter_livre(
        4,
        "Candide",
        "Voltaire",
        1759,
    )

    return biblio


def main() -> None:
    biblio = creer_bibliotheque()

    print("Liste des livres")
    biblio.afficher_livres()

    print()

    print("Emprunt du livre 2")
    if biblio.emprunter(2):
        print("Emprunt réussi")
    else:
        print("Impossible")

    print()

    print("Livres disponibles :", biblio.nombre_disponibles())

    print()

    resultat = biblio.chercher_par_titre("Le")

    for livre in resultat:
        print(livre["titre"])


if __name__ == "__main__":
    main()