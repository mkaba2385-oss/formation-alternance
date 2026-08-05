# Correction – Exercice 2 : Refactorer

Le code refactorisé est disponible dans le fichier **`refactorer.py`**.

## Changements apportés

### 1. Séparation des responsabilités (SRP)

La classe `GestionnaireDiagnostic` a été découpée en plusieurs classes ayant chacune une responsabilité unique :

- `TorchDiagnosticModel` : réalise le diagnostic à l'aide du modèle d'intelligence artificielle.
- `PostgresTraitementRepository` : récupère les traitements depuis la base de données.
- `PushNotifier` : envoie les notifications.
- `FileLogger` : écrit les journaux (logs).
- `DiagnosticService` : orchestre les différents services.

---

### 2. Utilisation d'abstractions (DIP)

Des interfaces ont été créées afin que le service métier ne dépende plus directement des implémentations concrètes :

- `DiagnosticModel`
- `TraitementRepository`
- `Notifier`
- `Logger`

Les implémentations concrètes peuvent ainsi être remplacées sans modifier le service.

---

### 3. Création d'un orchestrateur

La classe `DiagnosticService` coordonne les différentes opérations :

1. Analyse de la photo.
2. Récupération des traitements.
3. Envoi d'une notification.
4. Écriture d'un log.
5. Retour du résultat.

Elle ne contient aucune logique spécifique à une technologie particulière.

---

### 4. Respect des principes SOLID

| Principe | Application |
|----------|-------------|
| **SRP** | Chaque classe possède une seule responsabilité. |
| **OCP** | Il est possible d'ajouter une nouvelle base de données, un nouveau modèle IA ou un nouveau système de notification sans modifier `DiagnosticService`. |
| **LSP** | Les implémentations peuvent être remplacées par d'autres respectant la même interface. |
| **ISP** | Les interfaces sont petites et spécialisées (`DiagnosticModel`, `Notifier`, `Logger`, etc.). |
| **DIP** | `DiagnosticService` dépend uniquement des abstractions et non des implémentations concrètes. |

---

## Conclusion

Le refactoring répond aux objectifs de l'exercice :

- ✔ séparation du code en plusieurs classes spécialisées ;
- ✔ utilisation d'interfaces pour les dépendances externes ;
- ✔ création d'un orchestrateur simple ;
- ✔ respect des cinq principes **SOLID**.

**Le code complet est disponible dans le fichier `refactorer.py`.**