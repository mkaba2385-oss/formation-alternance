-- 1. Tables
CREATE TABLE produits (
    id SERIAL PRIMARY KEY,
    nom TEXT,
    prix NUMERIC(10,2),
    categorie_id INTEGER
);

CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    nom TEXT
);

-- 2. Générer 11 catégories
INSERT INTO categories (id, nom)
SELECT i, 'Catégorie ' || i
FROM generate_series(1, 11) AS i;

-- 3. Générer 100 000 produits
INSERT INTO produits (nom, prix, categorie_id)
SELECT
    'Produit ' || i,
    (random() * 1000)::NUMERIC(10,2),
    (random() * 10)::INTEGER + 1
FROM generate_series(1, 100000) AS i;

-- 4. Requête volontairement lente : aucun index sur prix
EXPLAIN ANALYZE
SELECT
    p.id,
    p.nom,
    p.prix,
    c.nom AS categorie
FROM produits p
JOIN categories c ON p.categorie_id = c.id
WHERE p.prix > 900
ORDER BY p.prix DESC;

-- 5. Ajouter un index
CREATE INDEX idx_produits_prix
ON produits(prix);

-- 6. Mesurer à nouveau
EXPLAIN ANALYZE
SELECT
    p.id,
    p.nom,
    p.prix,
    c.nom AS categorie
FROM produits p
JOIN categories c ON p.categorie_id = c.id
WHERE p.prix > 900
ORDER BY p.prix DESC;

-- 7. BONUS : index partiel
CREATE INDEX idx_produits_prix_eleve
ON produits(prix)
WHERE prix > 900;

-- 8. Mesurer avec l'index partiel
EXPLAIN ANALYZE
SELECT
    p.id,
    p.nom,
    p.prix,
    c.nom AS categorie
FROM produits p
JOIN categories c ON p.categorie_id = c.id
WHERE p.prix > 900
ORDER BY p.prix DESC;

