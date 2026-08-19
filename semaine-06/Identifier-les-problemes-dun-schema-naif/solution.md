
| Problème | Correction |
| --- | --- |
| `utilisateurs.info` contient plusieurs données | Séparer les colonnes |
| `parcelles.taille` mélange nombre + unité | `NUMERIC` + unité dans le nom |
| `observations` contient une liste | Créer `observations` |
| `proprietaire` n'est pas une FK  | `REFERENCES utilisateurs(numero)` |
| `diagnostics` n'a pas de PK | Ajouter `id PRIMARY KEY` |
