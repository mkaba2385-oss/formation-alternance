# Exercice 1 – Détecter les violations SOLID

## Analyse des violations

### 1. S — Single Responsibility Principle (SRP)

> **Principe :** Une classe ne doit avoir qu'une seule responsabilité (une seule raison de changer).

#### Pourquoi ce principe est-il violé ?

La classe `GestionnaireDiagnostic` cumule plusieurs responsabilités :

- Chargement et utilisation du modèle d'intelligence artificielle.
- Prétraitement de l'image.
- Exécution de l'inférence.
- Accès à la base de données pour récupérer les traitements.
- Envoi d'une notification push.
- Écriture des logs.
- Orchestration de toute la logique métier.

Chaque responsabilité peut évoluer indépendamment des autres. La classe possède donc **plusieurs raisons de changer**, ce qui viole le principe SRP.

#### Comment corriger ?

Découper la classe en plusieurs classes spécialisées :

- `DiagnosticModel` : réalise l'inférence IA.
- `TraitementRepository` : gère les accès à la base de données.
- `NotificationService` : envoie les notifications.
- `LoggerService` : écrit les journaux.
- `DiagnosticService` : orchestre les différents services.

---

## 2. D — Dependency Inversion Principle (DIP)

> **Principe :** Les modules de haut niveau doivent dépendre d'abstractions et non d'implémentations concrètes.

#### Pourquoi ce principe est-il violé ?

`GestionnaireDiagnostic` dépend directement de plusieurs technologies :

- `torch.load()` pour le modèle IA.
- `psycopg2.connect()` pour PostgreSQL.
- `requests.post()` pour les notifications.
- Le système de fichiers pour les logs.

Ces dépendances rendent le code :

- difficile à tester ;
- fortement couplé ;
- compliqué à faire évoluer.

#### Comment corriger ?

Créer des interfaces (abstractions) et injecter leurs implémentations :

- `DiagnosticModel`
- `Repository`
- `Notifier`
- `Logger`

Exemple :

```python
class DiagnosticService:
    def __init__(
        self,
        model: DiagnosticModel,
        repo: Repository,
        notifier: Notifier,
        logger: Logger,
    ):
        ...
```

Ainsi, il devient facile de remplacer PostgreSQL par MySQL, ou FCM par un autre système de notification.

---

## 3. O — Open/Closed Principle (OCP)

> **Principe :** Une classe doit être ouverte à l'extension mais fermée à la modification.

#### Pourquoi ce principe est-il violé ?

Pour modifier :

- la base de données ;
- le système de notification ;
- le modèle d'IA ;

il faut modifier directement le code de `GestionnaireDiagnostic`.

Chaque nouvelle technologie entraîne donc une modification du code existant, ce qui augmente le risque de régression.

#### Comment corriger ?

Créer des abstractions puis ajouter de nouvelles implémentations sans modifier la classe principale.

Par exemple :

- `PostgresRepository`
- `MySqlRepository`
- `MongoRepository`

ou encore :

- `FCMNotifier`
- `SmsNotifier`
- `EmailNotifier`

Le service utilisera simplement l'interface commune.

---

## 4. L — Liskov Substitution Principle (LSP)

> **Principe :** Une sous-classe doit pouvoir remplacer sa classe mère sans modifier le comportement attendu.

#### Pourquoi ce principe n'est-il pas violé ?

Dans cet extrait, aucune classe n'hérite d'une autre.

Il n'existe donc aucun risque de violer le contrat entre une classe mère et une classe fille.

#### Correction

Aucune correction n'est nécessaire dans cet exercice.

---

## 5. Interface Segregation Principle (ISP)

> **Principe :** Une classe ne doit pas être forcée d'implémenter des méthodes dont elle n'a pas besoin.

#### Pourquoi ce principe n'est-il pas violé ?

Le code ne définit aucune interface.

Il est donc impossible d'observer une violation de ce principe.

#### Correction

Si des interfaces sont créées, elles devront rester petites et spécialisées, par exemple :

- `Notifier`
- `Repository`
- `Logger`
- `DiagnosticModel`

plutôt qu'une énorme interface regroupant toutes les fonctionnalités.

---

# Résumé

| Principe | État | Justification |
|----------|------|---------------|
| **SRP** | **Violé** | La classe possède plusieurs responsabilités. |
| **DIP** | **Violé** | Dépend directement de PostgreSQL, Torch, FCM et du système de fichiers. |
| **OCP** | **Violé** | Chaque changement de technologie oblige à modifier la classe. |
| **LSP** | **Non violé** | Aucune hiérarchie de classes n'est présente. |
| **ISP** | **Non violé** | Aucune interface n'est utilisée dans ce code. |

## Conclusion

Les **trois violations principales** de cet exercice sont :

1. **SRP (Single Responsibility Principle)**
2. **DIP (Dependency Inversion Principle)**
3. **OCP (Open/Closed Principle)**

Les principes **LSP** et **ISP** ne sont pas concernés par cet extrait de code.