CREATE DATABASE IF NOT EXISTS abd;

USE abd;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT,
    revenue DECIMAL(10, 2)
);

INSERT INTO
    users (name, age, revenue)
VALUES ('Alice Dupont', 28, 45000.00),
    ('Bob Martin', 35, 62000.50),
    ('Claire Dubois', 42, 78500.00),
    ('David Leroy', 31, 53000.75),
    ('Emma Bernard', 26, 41000.00),
    (
        'François Petit',
        39,
        69000.25
    ),
    (
        'Gabrielle Roux',
        45,
        85000.00
    ),
    ('Hugo Moreau', 29, 48000.50),
    (
        'Isabelle Simon',
        33,
        58000.00
    ),
    (
        'Julien Laurent',
        38,
        72000.80
    );