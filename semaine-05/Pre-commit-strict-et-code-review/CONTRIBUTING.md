# CONTRIBUTING.md

## Pre-commit

J'ai mis en place **pre-commit** pour vérifier automatiquement le code avant chaque commit.

Les vérifications utilisées sont :

* `ruff format` pour le formatage
* `ruff check` pour vérifier le code
* `mypy --strict` pour vérifier les types
* `pytest` pour vérifier que les tests passent

J'ai aussi créé un hook personnalisé dans `check_code.py`.

Ce hook interdit :

* `print()`
* les `TODO` sans nom

Un TODO doit être écrit comme ceci :

```python
# TODO(moussa): améliorer cette fonction
```

Si une vérification échoue le commit est bloqué.

Pour lancer les vérifications manuellement :

```bash
pre-commit run --all-files
```

J'ai également testé des cas volontairement incorrects pour vérifier que les commits sont bien refusés.
