1
SELECT LastName, FirstName, EmployeeID FROM employees
2
SELECT LastName, FirstName, EmployeeID FROM employees WHERE City = "Seattle"
3
SELECT LastName, FirstName, EmployeeID FROM employees WHERE City = "London"
4
SELECT LastName, FirstName, Title FROM employees WHERE Title LIKE "%Sales%"
5
SELECT TitleOfCourtesy, LastName, FirstName FROM employees WHERE TitleOfCourtesy LIKE "%s%"
6
SELECT LastName, FirstName, BirthDate FROM employees ORDER BY BirthDate ASC LIMIT 5
7
SELECT LastName, FirstName, HireDate FROM employees ORDER BY HireDate ASC LIMIT 5
8
SELECT LastName, FirstName FROM employees WHERE ReportsTo ISNULL
9
SELECT (e.FirstName || " " ||  e.LastName) AS Employee, 
	(s.FirstName || " " || s.LastName) AS Manager
FROM employees e
INNER JOIN employees s ON s.EmployeeID = e.ReportsTo
10
SELECT COUNT(*) as "Number of Female Employees" FROM employees WHERE TitleOfCourtesy LIKE "%s%"
11
SELECT COUNT(*) as "Number of Male Employees" FROM employees WHERE TitleOfCourtesy Not LIKE "%s%"
12
SELECT City, Count(FirstName) as Total
FROM employees
GROUP BY City
13
SELECT orders.OrderID, (Employees.FirstName || " " ||  Employees.LastName) AS Employee 
FROM orders
INNER JOIN employees
ON orders.EmployeeID = employees.employeeID
14
SELECT orders.OrderID, shippers.CompanyName
FROM orders
INNER JOIN shippers
ON orders.ShipVia = shippers.ShipperID
15
SELECT ShipCountry, Count(ShipCountry) as Total
FROM orders
GROUP BY ShipCountry
ORDER BY Total DESC
16
SELECT (e.FirstName|| " " || e.LastName) as Name, COUNT(o.EmployeeID)  as cnt
FROM orders o
INNER JOIN employees e ON o.EmployeeID = e.EmployeeID
GROUP BY o.EmployeeID
ORDER BY cnt DESC
LIMIT 1
17
SELECT c.CompanyName as Name, COUNT(o.CustomerID)  as cnt
FROM orders o
INNER JOIN customers c ON o.CustomerID= c.CustomerID
GROUP BY o.CustomerID
ORDER BY cnt DESC
LIMIT 3
18
SELECT orders.OrderID, customers.CompanyName AS Customer, (employees.FirstName || " " ||  employees.LastName) AS Employee 
FROM orders
INNER JOIN employees
ON orders.EmployeeID = employees.EmployeeID
INNER JOIN customers
ON customers.CustomerID = orders.CustomerID
19
SELECT orders.OrderID, customers.CompanyName AS Customer, shippers.CompanyName as Shipper
FROM orders
INNER JOIN shippers
ON orders.ShipVia= Shippers.ShipperID
INNER JOIN customers
ON customers.CustomerID = orders.CustomerID
















