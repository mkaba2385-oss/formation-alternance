-- Nettoyage si le script est relancé
DROP TABLE IF EXISTS prix_sini;

-- 1. Création de la table
CREATE TABLE prix_sini (
    id SERIAL PRIMARY KEY,
    produit_id INTEGER NOT NULL,
    marche TEXT NOT NULL,
    date_prix DATE NOT NULL,
    prix NUMERIC(10,2) NOT NULL
);


INSERT INTO prix_sini (produit_id, marche, date_prix, prix)
SELECT
    p.produit_id,
    m.marche,
    d.date_prix,
    ROUND(
        (
            10
            + p.produit_id * 5
            + CASE WHEN m.marche = 'Mali' THEN 2 ELSE 0 END
            + (EXTRACT(DOY FROM d.date_prix)::INTEGER % 10)
            + random() * 4
        )::NUMERIC,
        2
    ) AS prix
FROM
    generate_series(1, 3) AS p(produit_id)
CROSS JOIN
    (VALUES ('Mali'), ('France')) AS m(marche)
CROSS JOIN
    generate_series(
        CURRENT_DATE - INTERVAL '39 days',
        CURRENT_DATE,
        INTERVAL '1 day'
    ) AS d(date_prix)
ORDER BY p.produit_id, m.marche, d.date_prix;


SELECT *
FROM prix_sini
ORDER BY produit_id, marche, date_prix
LIMIT 20;



SELECT
    produit_id,
    marche,
    date_prix,
    prix AS prix_courant,
    ROUND(
        AVG(prix) OVER (
            PARTITION BY produit_id, marche
            ORDER BY date_prix
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ),
        2
    ) AS moyenne_mobile_7_jours
FROM prix_sini
ORDER BY produit_id, marche, date_prix;




SELECT
    produit_id,
    marche,
    date_prix,
    prix,
    RANK() OVER (
        PARTITION BY produit_id, marche
        ORDER BY prix DESC
    ) AS rang_prix
FROM prix_sini
ORDER BY produit_id, marche, rang_prix;



SELECT
    produit_id,
    marche,
    date_prix,
    prix,
    LAG(prix) OVER (
        PARTITION BY produit_id, marche
        ORDER BY date_prix
    ) AS prix_precedent,
    ROUND(
        (
            (prix - LAG(prix) OVER (
                PARTITION BY produit_id, marche
                ORDER BY date_prix
            ))
            / NULLIF(
                LAG(prix) OVER (
                    PARTITION BY produit_id, marche
                    ORDER BY date_prix
                ),
                0
            )
        ) * 100,
        2
    ) AS variation_pourcent
FROM prix_sini
ORDER BY produit_id, marche, date_prix;



SELECT
    produit_id,
    marche,
    date_prix,
    prix,
    ROUND(
        SUM(prix) OVER (
            PARTITION BY produit_id, marche
            ORDER BY date_prix
            ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
        ),
        2
    ) AS prix_cumule_30_jours
FROM prix_sini
ORDER BY produit_id, marche, date_prix;


