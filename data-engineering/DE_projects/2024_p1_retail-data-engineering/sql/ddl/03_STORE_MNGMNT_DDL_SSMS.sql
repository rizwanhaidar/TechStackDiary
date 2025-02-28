/***********************************DDL********************************/
USE store_management;

DROP TABLE stores;
DROP TABLE employees;

CREATE TABLE stores (
    store_id VARCHAR(36) PRIMARY KEY,  -- Unique identifier for each store
    store_name VARCHAR(100) NOT NULL,  -- Name of the store
    address VARCHAR(255) NOT NULL,     -- Address of the store
    city VARCHAR(100) NOT NULL,        -- City where the store is located
    state VARCHAR(100) NOT NULL,       -- State where the store is located
    country VARCHAR(100) NOT NULL,     -- Country where the store is located
    postal_code VARCHAR(20) NOT NULL,  -- Postal code of the store
    manager_id VARCHAR(36),            -- Foreign key referencing the employees table
    contact_email VARCHAR(100),        -- Contact email for the store
    contact_phone VARCHAR(30),         -- Contact phone number for the store
    opening_date DATETIME NOT NULL,    -- Date when the store was opened
    store_closing_date DATETIME,       -- Date when the store was closed (NULL if active)
    is_active BIT DEFAULT 1           -- Indicates if the store is active (1) or closed (0)
);

CREATE TABLE employees (
    employee_id VARCHAR(36) PRIMARY KEY,  -- Unique identifier for each employee
    store_id VARCHAR(36) NOT NULL,        -- Foreign key referencing the stores table
    first_name VARCHAR(50) NOT NULL,      -- First name of the employee
    last_name VARCHAR(50) NOT NULL,       -- Last name of the employee
    role VARCHAR(50) NOT NULL,            -- Role of the employee (e.g., Store Manager, Cashier)
    superior_id VARCHAR(36),              -- Foreign key referencing the employee's superior
    hire_date DATETIME NOT NULL,          -- Date when the employee was hired
    salary DECIMAL(10, 2) NOT NULL,       -- Salary of the employee
    is_active BIT DEFAULT 1,              -- Indicates if the employee is active (1) or terminated (0)
);


ALTER TABLE stores 
ALTER COLUMN opening_date DATETIME2;

ALTER TABLE stores 
ALTER COLUMN store_closing_date DATETIME2;



