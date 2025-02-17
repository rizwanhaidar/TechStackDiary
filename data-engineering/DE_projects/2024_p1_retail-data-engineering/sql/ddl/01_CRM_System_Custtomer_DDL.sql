-- CREATE DATABASE CRM_System;
-- USE CRM_System;
-- USER rizwanhaidar
-- Pass ****123

CREATE TABLE CRM_System.customers (
    customer_id VARCHAR(36) PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    phone VARCHAR(20),
    address VARCHAR(255),
    loyalty_points INT
);

SELECT * FROM customers ;

SELECT count(*) FROM customers ;

SELECT * FROM CUSTOMERS LIMIT 10;



