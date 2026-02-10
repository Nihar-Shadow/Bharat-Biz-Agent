-- ============================================================
-- DEMO DATASET FOR INDIAN SMB BUSINESS SYSTEM
-- 10 Customers, 20 Products, Sample Orders
-- ============================================================

-- Clear existing data (optional)
DELETE FROM order_items;
DELETE FROM orders;
DELETE FROM products;
DELETE FROM customers;

-- ============================================================
-- CUSTOMERS (10 realistic Indian customers)
-- ============================================================

INSERT INTO customers (name, email, phone, address, created_at) VALUES
('Rahul Sharma', 'rahul.sharma@gmail.com', '9876543210', '123, MG Road, Connaught Place, New Delhi, Delhi 110001', datetime('now')),
('Priya Patel', 'priya.patel@yahoo.com', '9123456789', '456, Brigade Road, Bangalore, Karnataka 560001', datetime('now')),
('Amit Kumar', 'amit.kumar@outlook.com', '9988776655', '789, Park Street, Kolkata, West Bengal 700016', datetime('now')),
('Sneha Reddy', 'sneha.reddy@gmail.com', '9876512345', '321, Banjara Hills, Hyderabad, Telangana 500034', datetime('now')),
('Vikram Singh', 'vikram.singh@gmail.com', '9765432109', '654, Civil Lines, Jaipur, Rajasthan 302006', datetime('now')),
('Anjali Gupta', 'anjali.gupta@rediffmail.com', '9654321098', '987, Andheri West, Mumbai, Maharashtra 400058', datetime('now')),
('Rajesh Verma', 'rajesh.verma@gmail.com', '9543210987', '147, Gomti Nagar, Lucknow, Uttar Pradesh 226010', datetime('now')),
('Kavita Joshi', 'kavita.joshi@yahoo.com', '9432109876', '258, Satellite, Ahmedabad, Gujarat 380015', datetime('now')),
('Suresh Nair', 'suresh.nair@gmail.com', '9321098765', '369, MG Road, Kochi, Kerala 682016', datetime('now')),
('Deepa Iyer', 'deepa.iyer@outlook.com', '9210987654', '741, T Nagar, Chennai, Tamil Nadu 600017', datetime('now'));

-- ============================================================
-- PRODUCTS (20 items - Electronics & Office Supplies)
-- ============================================================

-- Electronics
INSERT INTO products (name, sku, price, stock_quantity, description, created_at) VALUES
('Dell Laptop i5 8GB', 'LAP-DELL-001', 45000.00, 15, 'Electronics - Dell Laptop i5 8GB', datetime('now')),
('HP Laptop i7 16GB', 'LAP-HP-002', 65000.00, 10, 'Electronics - HP Laptop i7 16GB', datetime('now')),
('Lenovo ThinkPad', 'LAP-LEN-003', 55000.00, 12, 'Electronics - Lenovo ThinkPad', datetime('now')),
('Logitech Wireless Mouse', 'MOU-LOG-001', 500.00, 50, 'Accessories - Logitech Wireless Mouse', datetime('now')),
('Dell Wired Mouse', 'MOU-DELL-002', 300.00, 75, 'Accessories - Dell Wired Mouse', datetime('now')),
('Mechanical Keyboard RGB', 'KEY-MEC-001', 2500.00, 30, 'Accessories - Mechanical Keyboard RGB', datetime('now')),
('Wireless Keyboard', 'KEY-WIR-002', 1200.00, 40, 'Accessories - Wireless Keyboard', datetime('now')),
('24-inch Dell Monitor', 'MON-DELL-001', 12000.00, 20, 'Electronics - 24-inch Dell Monitor', datetime('now')),
('27-inch LG Monitor', 'MON-LG-002', 18000.00, 15, 'Electronics - 27-inch LG Monitor', datetime('now')),
('1080p HD Webcam', 'WEB-HD-001', 2500.00, 25, 'Accessories - 1080p HD Webcam', datetime('now')),
('Noise Cancelling Headphones', 'HEAD-NC-001', 3500.00, 35, 'Accessories - Noise Cancelling Headphones', datetime('now')),
('USB-C Hub 7-in-1', 'HUB-USB-001', 1800.00, 45, 'Accessories - USB-C Hub 7-in-1', datetime('now'));

-- Office Supplies
INSERT INTO products (name, sku, price, stock_quantity, description, created_at) VALUES
('A4 Paper Ream (500 sheets)', 'PAP-A4-001', 250.00, 100, 'Stationery - A4 Paper Ream', datetime('now')),
('Ballpoint Pen Box (50 pcs)', 'PEN-BP-001', 150.00, 80, 'Stationery - Ballpoint Pen Box', datetime('now')),
('Stapler Heavy Duty', 'STA-HD-001', 350.00, 60, 'Stationery - Stapler Heavy Duty', datetime('now')),
('File Folders Pack (25)', 'FOL-FF-001', 400.00, 70, 'Stationery - File Folders Pack', datetime('now')),
('Whiteboard Markers (12 pcs)', 'MAR-WB-001', 300.00, 55, 'Stationery - Whiteboard Markers', datetime('now')),
('Desk Organizer', 'ORG-DESK-001', 800.00, 40, 'Office - Desk Organizer', datetime('now')),
('Calculator Scientific', 'CAL-SCI-001', 600.00, 45, 'Office - Calculator Scientific', datetime('now')),
('Printer Ink Cartridge', 'INK-HP-001', 1500.00, 30, 'Consumables - Printer Ink Cartridge', datetime('now'));

-- ============================================================
-- SAMPLE ORDERS (10 sample orders with items)
-- ============================================================

-- Order 1: Rahul Sharma - Laptop + Mouse
INSERT INTO orders (customer_id, status, total_amount, created_at) VALUES
(1, 'delivered', 45500.00, datetime('now', '-25 days'));

INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price) VALUES
(1, 1, 1, 45000.00, 45000.00),  -- Dell Laptop
(1, 4, 1, 500.00, 500.00);       -- Logitech Mouse

-- Order 2: Priya Patel - Monitor + Keyboard
INSERT INTO orders (customer_id, status, total_amount, created_at) VALUES
(2, 'delivered', 13200.00, datetime('now', '-20 days'));

INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price) VALUES
(2, 8, 1, 12000.00, 12000.00),   -- Dell Monitor
(2, 7, 1, 1200.00, 1200.00);     -- Wireless Keyboard

-- Order 3: Amit Kumar - Office Supplies
INSERT INTO orders (customer_id, status, total_amount, created_at) VALUES
(3, 'delivered', 1100.00, datetime('now', '-18 days'));

INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price) VALUES
(3, 13, 2, 250.00, 500.00),      -- A4 Paper
(3, 14, 2, 150.00, 300.00),      -- Pens
(3, 17, 1, 300.00, 300.00);      -- Markers

-- Order 4: Sneha Reddy - HP Laptop + Accessories
INSERT INTO orders (customer_id, status, total_amount, created_at) VALUES
(4, 'shipped', 71000.00, datetime('now', '-15 days'));

INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price) VALUES
(4, 2, 1, 65000.00, 65000.00),   -- HP Laptop
(4, 6, 1, 2500.00, 2500.00),     -- Mechanical Keyboard
(4, 11, 1, 3500.00, 3500.00);    -- Headphones

-- Order 5: Vikram Singh - Multiple Mice
INSERT INTO orders (customer_id, status, total_amount, created_at) VALUES
(5, 'delivered', 2500.00, datetime('now', '-12 days'));

INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price) VALUES
(5, 4, 5, 500.00, 2500.00);      -- 5x Logitech Mouse

-- Order 6: Anjali Gupta - LG Monitor + Webcam
INSERT INTO orders (customer_id, status, total_amount, created_at) VALUES
(6, 'confirmed', 20500.00, datetime('now', '-10 days'));

INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price) VALUES
(6, 9, 1, 18000.00, 18000.00),   -- LG Monitor
(6, 10, 1, 2500.00, 2500.00);    -- Webcam

-- Order 7: Rajesh Verma - Stationery Bulk
INSERT INTO orders (customer_id, status, total_amount, created_at) VALUES
(7, 'delivered', 2750.00, datetime('now', '-8 days'));

INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price) VALUES
(7, 13, 5, 250.00, 1250.00),     -- A4 Paper
(7, 15, 2, 350.00, 700.00),      -- Staplers
(7, 16, 2, 400.00, 800.00);      -- File Folders

-- Order 8: Kavita Joshi - Lenovo Laptop
INSERT INTO orders (customer_id, status, total_amount, created_at) VALUES
(8, 'pending', 55000.00, datetime('now', '-5 days'));

INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price) VALUES
(8, 3, 1, 55000.00, 55000.00);   -- Lenovo ThinkPad

-- Order 9: Suresh Nair - Accessories Bundle
INSERT INTO orders (customer_id, status, total_amount, created_at) VALUES
(9, 'confirmed', 8300.00, datetime('now', '-3 days'));

INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price) VALUES
(9, 6, 1, 2500.00, 2500.00),     -- Mechanical Keyboard
(9, 11, 1, 3500.00, 3500.00),    -- Headphones
(9, 12, 1, 1800.00, 1800.00),    -- USB-C Hub
(9, 4, 1, 500.00, 500.00);       -- Mouse

-- Order 10: Deepa Iyer - Office Setup
INSERT INTO orders (customer_id, status, total_amount, created_at) VALUES
(10, 'pending', 3900.00, datetime('now', '-1 days'));

INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price) VALUES
(10, 18, 1, 800.00, 800.00),     -- Desk Organizer
(10, 19, 2, 600.00, 1200.00),    -- Calculators
(10, 20, 1, 1500.00, 1500.00),   -- Ink Cartridge
(10, 14, 2, 150.00, 300.00),     -- Pens
(10, 13, 1, 250.00, 250.00);     -- A4 Paper

-- ============================================================
-- SUMMARY
-- ============================================================
-- Customers: 10
-- Products: 20 (12 Electronics/Accessories + 8 Office Supplies)
-- Orders: 10 sample orders with realistic items
-- Total Revenue: ₹215,750.00
-- 
-- Categories:
-- - Laptops: 3 models (₹45k - ₹65k)
-- - Monitors: 2 models (₹12k - ₹18k)
-- - Accessories: 7 items (₹300 - ₹3.5k)
-- - Stationery: 5 items (₹150 - ₹400)
-- - Office: 3 items (₹600 - ₹1.5k)
-- ============================================================
