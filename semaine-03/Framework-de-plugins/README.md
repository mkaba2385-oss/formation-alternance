# Framework de plugins

Ce framework permet d'ajouter facilement de nouveaux plugins grâce au décorateur `@register`.

## Ajouter un nouveau plugin en 3 étapes

### Étape 1 : Créer une fonction

Écrire une fonction contenant le code du plugin.

```python
def bonjour(nom):
    print(f"Bonjour {nom}")
```

---

### Étape 2 : Enregistrer le plugin

Ajouter le décorateur `@register("nom_du_plugin")` au-dessus de la fonction.

```python
@register("bonjour")
def bonjour(nom):
    print(f"Bonjour {nom}")
```

Le plugin est automatiquement enregistré dans le dictionnaire global `PLUGINS`.

---

### Étape 3 : Exécuter le plugin

Appeler la fonction `run_plugin()` en passant le nom du plugin et ses arguments.

```python
run_plugin("bonjour", "Alice")
```

Résultat :

```text
Bonjour Alice
```

---

## Exécuter un plugin uniquement en développement

Pour empêcher un plugin de s'exécuter en production, utiliser le décorateur `@only_if_env("dev")`.

```python
@register("sms")
@only_if_env("dev")
def envoyer_sms(numero, message):
    print(f"SMS envoyé à {numero}")
    print(f"Message : {message}")
```

Si la variable d'environnement `ENV` vaut `"dev"`, le plugin est exécuté.

```python
import os

os.environ["ENV"] = "dev"

run_plugin("sms", "0612345678", "Bonjour !")
```

Résultat :

```text
SMS envoyé à 0612345678
Message : Bonjour !
```

Si `ENV` vaut `"prod"`, le plugin n'est pas exécuté.

```python
import os

os.environ["ENV"] = "prod"

run_plugin("sms", "0612345678", "Bonjour !")
```

Résultat :

```text
Le plugin 'envoyer_sms' est désactivé (ENV=prod).
```