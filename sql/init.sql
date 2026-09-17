CREATE TABLE IF NOT EXISTS products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    barcode VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    cost_price DECIMAL(10, 2) NOT NULL,
    sale_price DECIMAL(10, 2) NOT NULL,
    current_stock DECIMAL(10, 2),
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    current_balance DECIMAL(10, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS suppliers (
    supplier_id int PRIMARY KEY AUTO_INCREMENT,
    company_name VARCHAR(255) NOT NULL,
    phone VARCHAR (10)
);

CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    user_role VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS cash_sessions (
    session_id int PRIMARY KEY AUTO_INCREMENT,
    user_id int,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    opened_at DATETIME,
    closed_at DATETIME NULL,
    initial_cash DECIMAL(10,2),
    estimated_cash DECIMAL(10,2),
    real_cash DECIMAL(10,2) NULL
);

CREATE TABLE IF NOT EXISTS sales (
    sale_id INT PRIMARY KEY AUTO_INCREMENT,
    session_id INT, 
    FOREIGN KEY (session_id) REFERENCES cash_sessions(session_id),
    customer_id INT, 
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    total DECIMAL(10,2),
    payment_method VARCHAR(200),
    payment_status VARCHAR(200),
    created_at DATETIME
);

CREATE TABLE IF NOT EXISTS sale_details(
detail_id INT PRIMARY KEY AUTO_INCREMENT,
sale_id INT, 
FOREIGN KEY (sale_id) REFERENCES sales(sale_id),
product_id INT, 
FOREIGN KEY (product_id) REFERENCES products(product_id),
quantity DECIMAL(10,2),
unit_price DECIMAL(10,2),
subtotal DECIMAL(10,2)
);


CREATE TABLE IF NOT EXISTS cash_movements (
    movement_id INT PRIMARY KEY AUTO_INCREMENT,
    session_id INT, 
    FOREIGN KEY (session_id) REFERENCES cash_sessions(session_id),
    supplier_id INT NULL, 
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id) ,
    movement_type VARCHAR(255),
    amount DECIMAL(10,2),
    description VARCHAR(255),
    created_at DATETIME 
);

