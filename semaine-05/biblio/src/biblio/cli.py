import argparse
from pathlib import Path

from .repository import LivreRepository
from .service import BibliothequeService


def creer_service() -> BibliothequeService:
    chemin = Path("bibliotheque.json")
    repository = LivreRepository(chemin)
    return BibliothequeService(repository)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Gestionnaire de bibliothèque")

    sous_commandes = parser.add_subparsers(
        dest="commande",
        required=True,
    )

    ajouter = sous_commandes.add_parser("ajouter")
    ajouter.add_argument("titre")
    ajouter.add_argument("auteur")
    ajouter.add_argument("annee", type=int)

    sous_commandes.add_parser("lister")

    chercher = sous_commandes.add_parser("chercher")
    chercher.add_argument("id", type=int)

    supprimer = sous_commandes.add_parser("supprimer")
    supprimer.add_argument("id", type=int)

    emprunter = sous_commandes.add_parser("emprunter")
    emprunter.add_argument("id", type=int)
    emprunter.add_argument("emprunteur")

    rendre = sous_commandes.add_parser("rendre")
    rendre.add_argument("id", type=int)

    args = parser.parse_args(argv)
    service = creer_service()

    if args.commande == "ajouter":
        livre = service.ajouter_livre(
            args.titre,
            args.auteur,
            args.annee,
        )
        print(f"Livre ajouté : {livre.id} - {livre.titre}")

    elif args.commande == "lister":
        livres = service.lister_livres()

        if not livres:
            print("Aucun livre dans la bibliothèque.")
            return

        for livre in livres:
            statut = "disponible" if livre.disponible else "emprunté"
            print(f"{livre.id} - {livre.titre} - {livre.auteur} ({livre.annee}) - {statut}")

    elif args.commande == "chercher":
        livre_trouve = service.chercher_livre(args.id)

        if livre_trouve is None:
            print("Livre introuvable.")
        else:
            print(livre_trouve)

    elif args.commande == "supprimer":
        if service.supprimer_livre(args.id):
            print("Livre supprimé.")
        else:
            print("Livre introuvable.")

    elif args.commande == "emprunter":
        try:
            emprunt = service.emprunter_livre(
                args.id,
                args.emprunteur,
            )
            print(
                f"Livre emprunté par {emprunt.emprunteur}. "
                f"Retour prévu le {emprunt.date_retour_prevue}."
            )
        except ValueError as erreur:
            print(f"Erreur : {erreur}")

    elif args.commande == "rendre":
        try:
            service.rendre_livre(args.id)
            print("Livre rendu.")
        except ValueError as erreur:
            print(f"Erreur : {erreur}")
