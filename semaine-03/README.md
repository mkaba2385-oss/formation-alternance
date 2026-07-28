# README – Comparaison entre les deux versions

## Comparaison des modifications

### 1. Remplacement de `range(len(...))` par `zip()`

**Avant**

```python
for i in range(len(notes)):
    print(eleves[i], notes[i])
```

**Après**

```python
for eleve, note in zip(eleves, notes):
    print(eleve, note)
```

**Pourquoi ?**

- Le code est plus lisible.
- On n'utilise plus les indices manuellement.
- Le risque d'erreur est réduit.


### 2. Remplacement de `append()` dans une boucle par une compréhension de liste

**Avant**

```python
resultats = []

for i in range(len(notes)):
    if notes[i] >= 10:
        resultats.append(eleves[i])
```

**Après**

```python
resultats = [eleve for eleve, note in zip(eleves, notes) if note >= 10]
```

**Pourquoi ?**

- Le code est plus court.
- La création de la liste est plus claire.
- Cette écriture est recommandée en Python.

### 3. Calcul manuel d'une somme remplacé par `sum()`

**Avant**

```python
total = 0

for note in notes:
    total += note
```

**Après**

```python
total = sum(notes)
```

**Pourquoi ?**

- Le code est plus simple.
- `sum()` est une fonction intégrée optimisée.
- Il y a moins de lignes de code.


### 4. Recherche du maximum remplacée par `max()`

**Avant**

```python
meilleure = notes[0]
meilleur_eleve = eleves[0]

for i in range(len(notes)):
    if notes[i] > meilleure:
        meilleure = notes[i]
        meilleur_eleve = eleves[i]
```

**Après**

```python
meilleur_eleve, meilleure = max(
    zip(eleves, notes),
    key=lambda x: x[1]
)
```

**Pourquoi ?**

- Plus besoin d'écrire une boucle.
- `max()` trouve directement l'élément recherché.
- Le code est plus compact et plus lisible.

### 5. Suppression de `== True`

**Avant**

```python
if (notes[i] >= 10) == True:
```

**Après**

```python
if note >= 10:
```

**Pourquoi ?**

- Comparer une condition à `True` est inutile.
- Le code est plus naturel à lire.
- Cette écriture respecte les recommandations du Zen de Python.

### 6. Utilisation des f-strings

**Avant**

```python
print("Moyenne :", moyenne)
```

**Après**

```python
print(f"Moyenne : {moyenne:.2f}")
```

**Pourquoi ?**

- Les f-strings sont plus modernes.
- Elles permettent un formatage simple des valeurs.
- L'affichage est plus propre.

## Conclusion

La version refactorisée est plus **lisible**, **courte** et **idiomatique**. Elle utilise les fonctionnalités propres à Python plutôt que des habitudes issues d'autres langages comme Java ou C.

Les principales améliorations sont :

- utilisation de `zip()` pour parcourir plusieurs listes ;
- compréhension de liste à la place de `append()` dans une boucle ;
- utilisation de `sum()` et `max()` au lieu de boucles manuelles ;
- suppression des comparaisons inutiles avec `True` ;
- utilisation des f-strings pour un affichage plus moderne.

Le résultat est un code plus facile à comprendre, à maintenir et conforme aux bonnes pratiques du langage Python.