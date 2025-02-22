CREATE DATABASE Inventory_mgmt_sys;
USE Inventory_mgmt_sys;
-- USER rizwanhaidar
-- Pass ****123
TRUNCATE TABLE Inventory_mgmt_sys.products;

CREATE TABLE products (
    product_id CHAR(36) PRIMARY KEY,  -- UUID stored as CHAR(36)
    product_name VARCHAR(255) NOT NULL,
    category ENUM('Electronics', 'Clothing', 'Home & Kitchen', 'Books', 'Toys') NOT NULL,
    brand VARCHAR(255),
    unit_price DECIMAL(10,2) NOT NULL,
    cost_price DECIMAL(10,2) NOT NULL,
    supplier_id CHAR(36) NOT NULL,  -- UUID stored as CHAR(36)
    sku VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    manufacturer VARCHAR(255),
    weight DECIMAL(5,2) NOT NULL,  -- Weight in kg with 2 decimal places
    dimensions VARCHAR(50),  -- Format: WxHxD cm
    is_active BOOLEAN DEFAULT TRUE,
    CONSTRAINT chk_price CHECK (cost_price <= unit_price)  -- Ensures cost price is not higher than unit price
);



SELECT * FROM products;

SELECT count(*) FROM products;

SELECT * FROM products LIMIT 10;



