CREATE DATABASE IF NOT EXISTS juegos CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE juegos;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS juegos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL
);

INSERT INTO juegos (nombre, descripcion, precio) VALUES
('The Legend of Zelda: Tears of the Kingdom', 'Aventura y exploracion en mundo abierto', 1399.00),
('Hollow Knight', 'Metroidvania de accion y exploracion', 349.00);
