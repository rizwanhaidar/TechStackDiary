CREATE DATABASE Inventory_mgmt_sys;
USE Inventory_mgmt_sys;
-- USER rizwanhaidar
-- Pass ****123

/**************************************************************************
***************************************************************************
Table Name: Products							***************************
***************************************************************************
***************************************************************************/
TRUNCATE TABLE Inventory_mgmt_sys.products;

CREATE TABLE Inventory_mgmt_sys.products (
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

/**************************************************************************
***************************************************************************
Table Name: Products							***************************
***************************************************************************
***************************************************************************/
TRUNCATE TABLE Inventory_mgmt_sys.suppliers;

CREATE TABLE Inventory_mgmt_sys.suppliers (
    supplier_id VARCHAR(36) PRIMARY KEY,
    supplier_name VARCHAR(100) NOT NULL,
    contact_name VARCHAR(100),
    contact_email VARCHAR(100),
    contact_phone VARCHAR(20),
    address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    postal_code VARCHAR(20),
    website VARCHAR(255),
    payment_terms VARCHAR(50),
    lead_time INT
);

SELECT * FROM Inventory_mgmt_sys.suppliers;

SELECT count(*) FROM Inventory_mgmt_sys.suppliers;

SELECT * FROM Inventory_mgmt_sys.suppliers LIMIT 10;

--#Verification
/*************************Check if the Supplier ID matches with the Supplier ID in products**********************************/
SELECT SUPS.SUPPLIER_ID, PRODS.SUPPLIER_ID FROM Inventory_mgmt_sys.SUPPLIERS SUPS
,Inventory_mgmt_sys.PRODUCTS PRODS;

SELECT COUNT(*) FROM Inventory_mgmt_sys.SUPPLIERS SUPS 
INNER JOIN Inventory_mgmt_sys.PRODUCTS PRODS 
ON SUPS.SUPPLIER_ID = PRODS.SUPPLIER_ID;

--#Conclusion
/**************** The results says that there is no relation between productes and suppliers based on the supplier id********************/

--#Action
UPDATE Inventory_mgmt_sys.products
SET supplier_id = (SELECT supplier_id FROM Inventory_mgmt_sys.suppliers ORDER BY RAND() LIMIT 1) where 1=1;


--#Verification
/*************************Check if the Supplier ID matches with the Supplier ID in products**********************************/
SELECT SUPS.SUPPLIER_ID, PRODS.SUPPLIER_ID FROM Inventory_mgmt_sys.SUPPLIERS SUPS
,Inventory_mgmt_sys.PRODUCTS PRODS;

SELECT COUNT(distinct sups.supplier_id) FROM Inventory_mgmt_sys.SUPPLIERS SUPS 
left JOIN Inventory_mgmt_sys.PRODUCTS PRODS 
ON SUPS.SUPPLIER_ID = PRODS.SUPPLIER_ID;

--#Conclusion
/**************** The results says that there is arelation between productes and suppliers based on the supplier id********************/


