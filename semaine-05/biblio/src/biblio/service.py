from datetime import date, timedelta

from .decorators import log_calls
from .models import Emprunt, Livre
from .repository import LivreRepository


class BibliothequeService:
    def __init__(self, repository: LivreRepository):
        self.repository = repository

    @log_calls
    def ajouter_livre(
        self,
        titre: str,
        auteur: str,
        annee: int,
    ) -> Livre:
        livres = self.repository.tous()

        nouvel_id = max((livre.id for livre in livres), default=0) + 1

        livre = Livre(
            id=nouvel_id,
            titre=titre,
            auteur=auteur,
            annee=annee,
        )

        self.repository.ajouter(livre)
        return livre

    @log_calls
    def lister_livres(self) -> list[Livre]:
        return self.repository.tous()

    @log_calls
    def chercher_livre(self, livre_id: int) -> Livre | None:
        return self.repository.trouver(livre_id)

    @log_calls
    def supprimer_livre(self, livre_id: int) -> bool:
        return self.repository.supprimer(livre_id)

    @log_calls
    def emprunter_livre(
        self,
        livre_id: int,
        emprunteur: str,
    ) -> Emprunt:
        livre = self.repository.trouver(livre_id)

        if livre is None:
            raise ValueError("Livre introuvable")

        if not livre.disponible:
            raise ValueError("Le livre est déjà emprunté")

        livre.disponible = False
        self.repository.mettre_a_jour(livre)

        aujourd_hui = date.today()

        return Emprunt(
            livre_id=livre_id,
            emprunteur=emprunteur,
            date_emprunt=aujourd_hui,
            date_retour_prevue=aujourd_hui + timedelta(days=14),
        )

    @log_calls
    def rendre_livre(self, livre_id: int) -> bool:
        livre = self.repository.trouver(livre_id)

        if livre is None:
            raise ValueError("Livre introuvable")

        if livre.disponible:
            raise ValueError("Le livre n'est pas emprunté")

        livre.disponible = True
        return self.repository.mettre_a_jour(livre)
