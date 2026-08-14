# Gestionnaire de bibliothèque

Projet réalisé en Python dans le cadre de la formation.

L'objectif est de créer un petit gestionnaire de bibliothèque utilisable depuis le terminal.

## Fonctionnalités

Le programme permet de :

- ajouter des livres
- lister les livres
- chercher un livre
- supprimer un livre
- emprunter un livre
- rendre un livre
- sauvegarder les données dans un fichier JSON

## Installation

Cloner le projet puis se placer dans le dossier :

```bash
cd biblio

Créer l'environnement virtuel :

python -m venv .venv

Activer l'environnement virtuel :

source .venv/bin/activate

Installer le projet :

pip install -e .

Installer les outils nécessaires au développement :

pip install pytest pytest-cov mypy ruff pre-commit

Installer les hooks pre-commit :

pre-commit install

Utilisation
Ajouter un livre
python -m biblio ajouter "1984" "George Orwell" 1949
Lister les livres
python -m biblio lister
Chercher un livre
python -m biblio chercher 1
Emprunter un livre
python -m biblio emprunter 1 Moussa
Rendre un livre
python -m biblio rendre 1
Supprimer un livre
python -m biblio supprimer 1

Les données de la bibliothèque sont sauvegardées dans le fichier bibliotheque.json.

Tests

Pour lancer les tests :

pytest

Le projet contient actuellement 26 tests.

Pour voir la couverture :

pytest --cov=src/biblio --cov-report=term-missing

La couverture actuelle est de 94 %.

Qualité du code

Le projet utilise plusieurs outils pour garder un code propre :

Ruff pour le linting et le formatage
Mypy en mode strict pour vérifier les types
Pytest pour les tests
Pre-commit pour lancer automatiquement les vérifications avant un commit
Pydantic pour les modèles de données

utilise ses commandes pour les verifications :

ruff check .
ruff format --check .
mypy src/ tests/
pytest

Les hooks pre-commit peuvent aussi être lancés avec :

pre-commit run --all-files
