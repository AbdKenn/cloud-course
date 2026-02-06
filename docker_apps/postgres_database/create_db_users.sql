CREATE DATABASE ma_base_de_donnees;


CREATE TABLE utilisateurs (
    id SERIAL PRIMARY KEY,          -- identifiant unique auto-incrémenté
    nom VARCHAR(50) NOT NULL,       -- nom de l'utilisateur
    email VARCHAR(100) UNIQUE NOT NULL, -- email unique
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- date de création
);


INSERT INTO utilisateurs (nom, email) 
VALUES ('Alice Dupont', 'alice.dupont@example.com');

-- 5️⃣ Vérifier les données
SELECT * FROM utilisateurs;

