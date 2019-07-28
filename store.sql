CREATE DATABASE store;
USE store;
CREATE TABLE categories (
id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
name VARCHAR(30)  UNIQUE NOT NULL
);
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    title VARCHAR(30) UNIQUE NOT NULL,
    description VARCHAR(100),
    price FLOAT NOT NULL,
    img_url VARCHAR(150),
    category_id INT,
    FOREIGN KEY (category_id)
        REFERENCES categories (id)
        ON DELETE CASCADE
    ON UPDATE CASCADE,
    favorite BOOLEAN
);