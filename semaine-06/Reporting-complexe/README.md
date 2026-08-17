# S6-J26 — Reporting complexe avec SQL

## Dataset

J'ai utilisé le dataset **Chinook** avec SQLite.

---

## 1. Revenus mensuels

### Objectif
Calculer le chiffre d'affaires total pour chaque mois.

### Méthode
J'utilise `strftime('%Y-%m', InvoiceDate)` pour regrouper les factures par mois et `SUM(Total)` pour calculer les revenus.

L'énoncé demandait 2010-2013 mais le dataset fourni contient des factures à partir de 2021.

## 2. Top 10 des clients par chiffre d'affaires cumulé

### Objectif
Trouver les 10 clients ayant généré le plus de chiffre d'affaires.

### Méthode
J'ai relié `Customer` et `Invoice` avec `CustomerId`, puis utilisé `SUM(i.Total)`, `GROUP BY`, `ORDER BY DESC` et `LIMIT 10`.

### Résultat

| Client | Chiffre d'affaires |
|---|---:|
| Helena Holý | 49.62 € |
| Richard Cunningham | 47.62 € |
| Luis Rojas | 46.62 € |
| Ladislav Kovács | 45.62 € |
| Hugh O'Reilly | 45.62 € |
| Frank Ralston | 43.62 € |
| Julia Barnett | 43.62 € |
| Fynn Zimmermann | 43.62 € |
| Astrid Gruber | 42.62 € |
| Victor Stevens | 42.62 € |

---

## 3. Genre le plus populaire par pays

### Objectif
Trouver, pour chaque pays, le genre musical ayant le plus de ventes.

### Méthode
J'ai relié `Customer`, `Invoice`, `InvoiceLine`, `Track` et `Genre`.

J'ai compté les ventes par pays et par genre, puis utilisé une CTE avec `ROW_NUMBER()` pour classer les genres dans chaque pays. Enfin, j'ai gardé le rang `1`.

### Résultat

Le genre dominant est principalement **Rock**.

Exemples :

- Argentina → Rock : 9 ventes
- Australia → Rock : 22 ventes
- Brazil → Rock : 81 ventes
- Canada → Rock : 107 ventes
- France → Rock : 65 ventes
- USA → Rock : 157 ventes
- Sweden → Latin : 12 ventes

---

## 4. Durée moyenne des tracks par artiste

### Objectif
Calculer la durée moyenne des morceaux pour chaque artiste.

### Méthode
J'ai relié `Artist` → `Album` → `Track`.

J'ai utilisé `AVG(t.Milliseconds)` puis divisé par `60000` pour convertir les millisecondes en minutes.

### Résultat

| Artiste | Durée moyenne |
|---|---:|
| Battlestar Galactica (Classic) | 48.76 min |
| Battlestar Galactica | 46.17 min |
| Heroes | 43.32 min |
| Lost | 43.17 min |
| Aquaman | 41.41 min |

---

## 5. Évolution des ventes par genre

### Objectif
Observer l'évolution du nombre de ventes par genre et par année.

### Méthode
J'ai relié `Invoice` → `InvoiceLine` → `Track` → `Genre`.

J'ai utilisé `strftime('%Y', InvoiceDate)` pour récupérer l'année et `COUNT()` pour compter les ventes.

### Résultat

Le genre **Rock** est le plus vendu chaque année dans les données obtenues.

| Année | Genre | Ventes |
|---|---|---:|
| 2021 | Rock | 180 |
| 2021 | Latin | 83 |
| 2022 | Rock | 157 |
| 2022 | Latin | 78 |
| 2023 | Rock | 158 |
| 2024 | Rock | 164 |
| 2025 | Rock | 176 |
| 2025 | Latin | 80 |

---

## Notions SQL utilisées

- `SELECT`
- `JOIN`
- `WHERE`
- `GROUP BY`
- `HAVING`
- `ORDER BY`
- `LIMIT`
- `COUNT()`
- `SUM()`
- `AVG()`
- `MAX()`
- `ROUND()`
- `strftime()`
- CTE avec `WITH`
- `ROW_NUMBER() OVER (...)`

## Conclusion

Ces exercices m'ont permis de pratiquer les requêtes SQL sur plusieurs tables et de construire des analyses plus complexes.

J'ai surtout travaillé sur les `JOIN`, les regroupements avec `GROUP BY`, les fonctions d'agrégation (`COUNT`, `SUM`, `AVG`) et les CTE pour réaliser des requêtes de reporting en SQL uniquement.
