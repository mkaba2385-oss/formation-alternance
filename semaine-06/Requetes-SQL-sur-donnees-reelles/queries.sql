-- 1. Les 5 artistes avec le plus d'albums

SELECT
    a.Name AS artiste,
    COUNT(al.AlbumId) AS nombre_albums
FROM Artist a
JOIN Album al ON a.ArtistId = al.ArtistId
GROUP BY a.ArtistId, a.Name
ORDER BY nombre_albums DESC
LIMIT 5;

-- Résultat obtenu avec la base utilisée pendant l'exercice :
-- Iron Maiden|21
-- Led Zeppelin|14
-- Deep Purple|11
-- Metallica|10
-- U2|10  


-- 2. Les factures supérieures à 10 €
SELECT
    InvoiceId,
    CustomerId,
    InvoiceDate,
    BillingCountry,
    Total
FROM Invoice
WHERE Total > 10
ORDER BY Total DESC;


-- 3. Nombre de clients par pays
SELECT
    Country,
    COUNT(CustomerId) AS nombre_clients
FROM Customer
GROUP BY Country
ORDER BY nombre_clients DESC, Country ASC;


-- 4. Titre le plus long par genre
-- "Plus long" signifie ici le nombre de caractères du titre.
SELECT
    g.Name AS genre,
    MAX(LENGTH(t.Name)) AS longueur_max_titre
FROM Track t
JOIN Genre g ON t.GenreId = g.GenreId
GROUP BY g.GenreId, g.Name
ORDER BY longueur_max_titre DESC;


-- 5. Genres ayant plus de 100 morceaux
SELECT
    g.Name AS genre,
    COUNT(t.TrackId) AS nombre_morceaux
FROM Genre g
JOIN Track t ON g.GenreId = t.GenreId
GROUP BY g.GenreId, g.Name
HAVING COUNT(t.TrackId) > 100
ORDER BY nombre_morceaux DESC;


-- 6. Top 10 des clients par chiffre d'affaires cumulé
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


-- 7. Chiffre d'affaires total par pays
SELECT
    c.Country,
    ROUND(SUM(i.Total), 2) AS chiffre_affaires
FROM Customer c
JOIN Invoice i ON c.CustomerId = i.CustomerId
GROUP BY c.Country
ORDER BY chiffre_affaires DESC;


-- 8. Top 10 des genres avec le plus de morceaux
SELECT
    g.Name AS genre,
    COUNT(t.TrackId) AS nombre_morceaux
FROM Genre g
JOIN Track t ON g.GenreId = t.GenreId
GROUP BY g.GenreId, g.Name
ORDER BY nombre_morceaux DESC
LIMIT 10;


-- 9. Artistes ayant plus de 10 albums
SELECT
    a.Name AS artiste,
    COUNT(al.AlbumId) AS nombre_albums
FROM Artist a
JOIN Album al ON a.ArtistId = al.ArtistId
GROUP BY a.ArtistId, a.Name
HAVING COUNT(al.AlbumId) > 10
ORDER BY nombre_albums DESC;


-- 10. Durée moyenne des morceaux par artiste
SELECT
    a.Name AS artiste,
    ROUND(AVG(t.Milliseconds) / 60000.0, 2) AS duree_moyenne_minutes
FROM Artist a
JOIN Album al ON a.ArtistId = al.ArtistId
JOIN Track t ON al.AlbumId = t.AlbumId
GROUP BY a.ArtistId, a.Name
ORDER BY duree_moyenne_minutes DESC;