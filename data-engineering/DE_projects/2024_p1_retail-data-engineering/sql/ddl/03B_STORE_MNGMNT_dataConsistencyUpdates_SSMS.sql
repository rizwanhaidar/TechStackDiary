/***********************DATA CONSISTENCY CHECKS AND CORRECTIONS***********************/
SELECT COUNT(*) FROM stores;
SELECT COUNT(*) FROM employees;

SELECT TOP 10 * FROM stores;


SELECT COUNT(*) FROM stores WHERE store_closing_date < opening_date AND is_active = 0;
--None of the active stores has a closing date prior to the opening date

SELECT COUNT(*) FROM stores WHERE store_closing_date < opening_date AND is_active = 1;
--All active stores must have a closing date less than the opening date

SELECT COUNT(*) FROM stores WHERE is_active = 1;
--242 equals the number of stores having a closing date less than the opening date


SELECT TOP 10 * FROM employees;

SELECT TOP 10 * FROM employees where role = 'Store Manager' and superior_id is not null;

SELECT TOP 10 * FROM employees where role = 'Store Manager' and superior_id is null;

select count(*) from stores s 
inner join employees e
on s.store_id = e.store_id --and s.manager_id = e.employee_id 
where --s.is_active = 0 and 
e.hire_date not between s.opening_date and s.store_closing_date;

SELECT COUNT(*) fROM (

SELECT distinct employee_id, e.hire_date, s.opening_date, s.store_closing_date
FROM stores s
INNER JOIN employees e ON s.store_id = e.store_id
WHERE e.hire_date <s.opening_date or (e.hire_date > s.store_closing_date and store_closing_date <> '0001-01-01')
)a;


SELECT distinct employee_id, e.hire_date, s.opening_date, s.store_closing_date
FROM stores s
INNER JOIN employees e ON s.store_id = e.store_id
WHERE e.hire_date <s.opening_date 
;

WITH InvalidHires AS (
    SELECT distinct employee_id, e.hire_date, s.opening_date, s.store_closing_date
		FROM stores s
		INNER JOIN employees e ON s.store_id = e.store_id
		WHERE e.hire_date <s.opening_date 
		OR
		(e.hire_date > s.store_closing_date and store_closing_date <> '0001-01-01')
)
UPDATE e
SET hire_date = DATEADD(
    DAY, 
    ABS(CHECKSUM(NEWID())) % NULLIF(DATEDIFF(DAY, ih.opening_date, ih.store_closing_date), 0), 
    ih.opening_date
)
FROM employees e
INNER JOIN InvalidHires ih ON e.employee_id = ih.employee_id;


SELECT e.*
FROM employees e
LEFT JOIN stores s ON e.store_id = s.store_id
WHERE s.store_id IS NULL AND e.store_id IS NOT NULL; -- added check for null store ids.


SELECT e.*, s.store_closing_date
FROM employees e
JOIN stores s ON e.store_id = s.store_id
WHERE s.store_closing_date <> '0001-01-01' AND e.hire_date > s.store_closing_date;

SELECT e.*, s.store_id AS store_store_id
FROM employees e
JOIN stores s ON e.employee_id = s.manager_id
WHERE e.store_id != s.store_id AND e.role = 'Store Manager';


SELECT s.*
FROM stores s
LEFT JOIN employees e ON s.manager_id = e.employee_id
WHERE e.employee_id IS NULL OR e.role != 'Store Manager';


SELECT e.*
FROM employees e
LEFT JOIN employees s ON e.superior_id = s.employee_id
WHERE e.superior_id IS NOT NULL AND s.employee_id IS NULL;

SELECT e.*, s.store_id AS superior_store_id
FROM employees e
JOIN employees s ON e.superior_id = s.employee_id
WHERE e.store_id != s.store_id AND e.superior_id IS NOT NULL;

SELECT *
FROM employees
WHERE store_id IS NULL AND role != 'Store Manager';