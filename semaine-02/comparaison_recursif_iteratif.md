# Comparaison des versions récursives et itératives

## Exercice 1 – Somme des chiffres

### Version récursive
- Plus courte et proche du raisonnement mathématique.
- Utilise des appels récursifs jusqu'au cas de base.

### Version itérative
- Utilise une boucle `while`.
- Ne crée pas d'appels de fonctions supplémentaires.

### Comparaison
- **Lisibilité :** la version récursive est élégante et concise, tandis que la version itérative est plus directe.
- **Longueur :** la version récursive est légèrement plus courte.
- **Performance :** la version itérative est plus performante, car elle évite les appels récursifs et consomme moins de mémoire.



## Exercice 2 – PGCD

### Version récursive
- Reproduit directement l'algorithme d'Euclide.
- Le code est compact et facile à comprendre.

### Version itérative
- Utilise une boucle `while` jusqu'à ce que le reste soit égal à 0.

### Comparaison
- **Lisibilité :** les deux versions sont simples à comprendre.
- **Longueur :** les deux versions ont une longueur similaire.
- **Performance :** la version itérative est légèrement plus efficace, car elle n'utilise pas la pile d'appels.


## Exercice 3 – Tri fusion

### Version récursive
- Découpe la liste en deux parties jusqu'à obtenir des listes d'un seul élément.
- Fusionne ensuite les sous-listes triées.

### Version itérative
- Fusionne progressivement des groupes de taille 1, puis 2, puis 4, etc.
- Le code est plus long et plus complexe à écrire.

### Comparaison
- **Lisibilité :** la version récursive est beaucoup plus facile à comprendre.
- **Longueur :** la version itérative est plus longue et demande davantage de code.
- **Performance :** les deux versions ont une complexité en **O(n log n)**. La version itérative peut être légèrement plus rapide, car elle évite les appels récursifs.



# Conclusion

La version récursive est particulièrement adaptée lorsque le problème est naturellement récursif, comme les arbres, les dossiers, les listes imbriquées ou les algorithmes de type *diviser pour régner* (par exemple le tri fusion). Elle permet d'écrire un code plus clair, plus concis et plus proche du raisonnement utilisé pour résoudre le problème.

En revanche, lorsque le traitement est simple ou que la profondeur de récursion peut devenir importante, la version itérative est généralement préférable. Elle est plus performante, consomme moins de mémoire et ne risque pas de dépasser la limite de récursion de Python.

Dans ce travail, la récursivité apporte un réel avantage pour le tri fusion, tandis que les versions itératives sont plus adaptées pour la somme des chiffres et le calcul du PGCD.