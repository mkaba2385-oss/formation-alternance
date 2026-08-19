
CREATE TABLE cooperatives (
    id INTEGER PRIMARY KEY,
    nom TEXT NOT NULL,
    region TEXT NOT NULL,
    president_id INTEGER NOT NULL,

    FOREIGN KEY (president_id)
        REFERENCES utilisateurs(id)
);


CREATE TABLE cooperative_members (
    cooperative_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,

    PRIMARY KEY (cooperative_id, user_id),

    FOREIGN KEY (cooperative_id)
        REFERENCES cooperatives(id)
        ON DELETE CASCADE,

    FOREIGN KEY (user_id)
        REFERENCES utilisateurs(id)
        ON DELETE CASCADE
);



CREATE TABLE bulk_sales (
    id INTEGER PRIMARY KEY,
    cooperative_id INTEGER NOT NULL,
    date_vente TIMESTAMP NOT NULL,
    produit TEXT NOT NULL,
    prix_negocie NUMERIC(12,2) NOT NULL,

    FOREIGN KEY (cooperative_id)
        REFERENCES cooperatives(id)
);


CREATE TABLE bulk_sale_contributions (
    bulk_sale_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    quantite NUMERIC(12,2) NOT NULL,

    PRIMARY KEY (bulk_sale_id, user_id),

    FOREIGN KEY (bulk_sale_id)
        REFERENCES bulk_sales(id)
        ON DELETE CASCADE,

    FOREIGN KEY (user_id)
        REFERENCES utilisateurs(id)
        ON DELETE CASCADE
);

