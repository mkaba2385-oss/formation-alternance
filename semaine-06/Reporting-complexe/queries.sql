
-- 1. Revenus mensuels entre 2010 et 2013
SELECT
    strftime('%Y-%m', InvoiceDate) AS mois,
    ROUND(SUM(Total), 2) AS revenus
FROM Invoice
WHERE InvoiceDate >= '2010-01-01'
  AND InvoiceDate < '2014-01-01'
GROUP BY mois
ORDER BY mois;


-- 2. Top 10 clients par chiffre d'affaires cumulé
SELECT
    c.CustomerId,
    c.FirstName,
    c.LastName,
    ROUND(SUM(i.Total), 2) AS chiffre_affaires
FROM Customer c
JOIN Invoice i ON c.CustomerId = i.CustomerId
GROUP BY c.CustomerId, c.FirstName, c.LastName
ORDER BY chiffre_affaires DESC
LIMIT 10;


-- 3. Genre le plus populaire par pays
WITH ventes AS (
    SELECT
        c.Country AS pays,
        g.Name AS genre,
        COUNT(il.InvoiceLineId) AS nombre_ventes
    FROM Customer c
    JOIN Invoice i
        ON c.CustomerId = i.CustomerId
    JOIN InvoiceLine il
        ON i.InvoiceId = il.InvoiceId
    JOIN Track t
        ON il.TrackId = t.TrackId
    JOIN Genre g
        ON t.GenreId = g.GenreId
    GROUP BY c.Country, g.GenreId, g.Name
),
classement AS (
    SELECT
        pays,
        genre,
        nombre_ventes,
        ROW_NUMBER() OVER (
            PARTITION BY pays
            ORDER BY nombre_ventes DESC
        ) AS rang
    FROM ventes
)
SELECT
    pays,
    genre,
    nombre_ventes
FROM classement
WHERE rang = 1
ORDER BY pays;


-- 4. Durée moyenne des tracks par artiste
SELECT
    a.ArtistId,
    a.Name AS artiste,
    ROUND(AVG(t.Milliseconds) / 60000.0, 2)
        AS duree_moyenne_minutes
FROM Artist a
JOIN Album al
    ON a.ArtistId = al.ArtistId
JOIN Track t
    ON al.AlbumId = t.AlbumId
GROUP BY a.ArtistId, a.Name
ORDER BY duree_moyenne_minutes DESC;


-- 5. Évolution annuelle des ventes par genre
SELECT
    strftime('%Y', i.InvoiceDate) AS annee,
    g.Name AS genre,
    COUNT(il.InvoiceLineId) AS nombre_ventes
FROM Invoice i
JOIN InvoiceLine il
    ON i.InvoiceId = il.InvoiceId
JOIN Track t
    ON il.TrackId = t.TrackId
JOIN Genre g
    ON t.GenreId = g.GenreId
GROUP BY annee, g.GenreId, g.Name
ORDER BY annee, nombre_ventes DESC;