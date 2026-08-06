# patterns-in-the-wild.md

# Détection de Design Patterns dans la bibliothèque Requests

## 1. Factory

**Pattern :** Factory

**Emplacement :**
- requests/sessions.py
- Fonction : `Session.request()`

**Description :**
La méthode `request()` crée automatiquement un objet `Request`, le prépare en `PreparedRequest`, puis l'envoie. Le code utilisateur n'a pas besoin de créer ces objets lui-même.

**Problème résolu :**
Le pattern Factory masque la logique de création des objets et simplifie leur utilisation.

---

## 2. Strategy

**Pattern :** Strategy

**Emplacement :**
- requests/adapters.py
- Classe : `HTTPAdapter`

**Description :**
Requests permet de changer l'adaptateur HTTP utilisé (`HTTPAdapter`). Selon l'adaptateur installé, la stratégie d'envoi des requêtes peut varier sans modifier le reste du code.

**Problème résolu :**
Permet de remplacer l'algorithme d'envoi des requêtes sans modifier la classe `Session`.

---

## 3. Singleton

**Pattern :** Singleton

**Emplacement :**
- requests/api.py
- Variable globale : `sessions.Session()`

**Description :**
Les fonctions de haut niveau comme `requests.get()` ou `requests.post()` utilisent une session créée automatiquement afin de partager certains paramètres et connexions.

**Problème résolu :**
Évite de recréer une nouvelle session pour chaque appel et centralise la gestion des connexions HTTP.

---

# Conclusion

La bibliothèque Requests utilise plusieurs design patterns afin de rendre son API simple à utiliser tout en restant flexible. Les principaux patterns observés sont Factory pour la création des requêtes, Strategy pour le choix de l'adaptateur HTTP et un comportement proche du Singleton pour la gestion des sessions.