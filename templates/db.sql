--This file contains your SQL code for creating the database and the users table using  sql     

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    username VARCHAR(50) UNIQUE,
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255),  -- store hashed password
    birthdate DATE,
    profile_image VARCHAR(255),
    phone VARCHAR(20),
    id_verified BOOLEAN DEFAULT FALSE,
    subscription_status VARCHAR(20) DEFAULT 'Inactive',
    join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
