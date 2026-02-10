# 📊 DEMO DATASET DOCUMENTATION

## 🎯 Overview

Realistic Indian SMB business demo dataset with:
- ✅ **10 Customers** - Indian names, realistic addresses
- ✅ **20 Products** - Electronics & Office Supplies
- ✅ **50 Orders** - Distributed over 30 days
- ✅ **Realistic Pricing** - Indian Rupees (₹)

---

## 🚀 Quick Start

### **Option 1: Python Seed Script (Recommended)**
```powershell
python seed_demo_data.py
```

### **Option 2: SQL Script**
```powershell
# SQLite
sqlite3 business.db < demo_data.sql

# Or use DB browser to import
```

---

## 👥 CUSTOMERS (10)

### **North India**
1. **Rahul Sharma** - Delhi
   - Phone: 9876543210
   - Email: rahul.sharma@gmail.com

2. **Vikram Singh** - Jaipur
   - Phone: 9765432109
   - Email: vikram.singh@gmail.com

3. **Rajesh Verma** - Lucknow
   - Phone: 9543210987
   - Email: rajesh.verma@gmail.com

### **South India**
4. **Priya Patel** - Bangalore
   - Phone: 9123456789
   - Email: priya.patel@yahoo.com

5. **Sneha Reddy** - Hyderabad
   - Phone: 9876512345
   - Email: sneha.reddy@gmail.com

6. **Suresh Nair** - Kochi
   - Phone: 9321098765
   - Email: suresh.nair@gmail.com

7. **Deepa Iyer** - Chennai
   - Phone: 9210987654
   - Email: deepa.iyer@outlook.com

### **East India**
8. **Amit Kumar** - Kolkata
   - Phone: 9988776655
   - Email: amit.kumar@outlook.com

### **West India**
9. **Anjali Gupta** - Mumbai
   - Phone: 9654321098
   - Email: anjali.gupta@rediffmail.com

10. **Kavita Joshi** - Ahmedabad
    - Phone: 9432109876
    - Email: kavita.joshi@yahoo.com

---

## 📦 PRODUCTS (20)

### **Laptops (3 models)**
| Product | SKU | Price | Stock |
|---------|-----|-------|-------|
| Dell Laptop i5 8GB | LAP-DELL-001 | ₹45,000 | 15 |
| HP Laptop i7 16GB | LAP-HP-002 | ₹65,000 | 10 |
| Lenovo ThinkPad | LAP-LEN-003 | ₹55,000 | 12 |

### **Monitors (2 models)**
| Product | SKU | Price | Stock |
|---------|-----|-------|-------|
| 24-inch Dell Monitor | MON-DELL-001 | ₹12,000 | 20 |
| 27-inch LG Monitor | MON-LG-002 | ₹18,000 | 15 |

### **Accessories (7 items)**
| Product | SKU | Price | Stock |
|---------|-----|-------|-------|
| Logitech Wireless Mouse | MOU-LOG-001 | ₹500 | 50 |
| Dell Wired Mouse | MOU-DELL-002 | ₹300 | 75 |
| Mechanical Keyboard RGB | KEY-MEC-001 | ₹2,500 | 30 |
| Wireless Keyboard | KEY-WIR-002 | ₹1,200 | 40 |
| 1080p HD Webcam | WEB-HD-001 | ₹2,500 | 25 |
| Noise Cancelling Headphones | HEAD-NC-001 | ₹3,500 | 35 |
| USB-C Hub 7-in-1 | HUB-USB-001 | ₹1,800 | 45 |

### **Stationery (5 items)**
| Product | SKU | Price | Stock |
|---------|-----|-------|-------|
| A4 Paper Ream (500 sheets) | PAP-A4-001 | ₹250 | 100 |
| Ballpoint Pen Box (50 pcs) | PEN-BP-001 | ₹150 | 80 |
| Stapler Heavy Duty | STA-HD-001 | ₹350 | 60 |
| File Folders Pack (25) | FOL-FF-001 | ₹400 | 70 |
| Whiteboard Markers (12 pcs) | MAR-WB-001 | ₹300 | 55 |

### **Office Supplies (3 items)**
| Product | SKU | Price | Stock |
|---------|-----|-------|-------|
| Desk Organizer | ORG-DESK-001 | ₹800 | 40 |
| Calculator Scientific | CAL-SCI-001 | ₹600 | 45 |
| Printer Ink Cartridge | INK-HP-001 | ₹1,500 | 30 |

---

## 📊 SAMPLE ORDERS

### **Order Distribution**
- **50 orders** generated over **30 days**
- **1-4 items** per order
- **Random quantities** (1-5 units)
- **Realistic status progression**:
  - Older orders (>7 days): Mostly "delivered"
  - Recent orders (<7 days): "pending", "confirmed", "shipped"

### **Sample Order Examples**

#### **Order 1: Rahul Sharma**
- **Date**: 25 days ago
- **Status**: Delivered
- **Items**:
  - Dell Laptop i5 8GB × 1 = ₹45,000
  - Logitech Wireless Mouse × 1 = ₹500
- **Total**: ₹45,500

#### **Order 2: Priya Patel**
- **Date**: 20 days ago
- **Status**: Delivered
- **Items**:
  - 24-inch Dell Monitor × 1 = ₹12,000
  - Wireless Keyboard × 1 = ₹1,200
- **Total**: ₹13,200

#### **Order 4: Sneha Reddy**
- **Date**: 15 days ago
- **Status**: Shipped
- **Items**:
  - HP Laptop i7 16GB × 1 = ₹65,000
  - Mechanical Keyboard RGB × 1 = ₹2,500
  - Noise Cancelling Headphones × 1 = ₹3,500
- **Total**: ₹71,000

---

## 💰 BUSINESS METRICS

### **Revenue**
- **Total Revenue**: ~₹2,00,000 - ₹3,00,000
- **Average Order Value**: ₹4,000 - ₹6,000
- **Orders per Customer**: 3-7 orders

### **Inventory**
- **Total Products**: 20
- **Total Stock Value**: ~₹15,00,000
- **Categories**: 4 (Electronics, Accessories, Stationery, Office)

### **Customer Distribution**
- **North India**: 3 customers
- **South India**: 4 customers
- **East India**: 1 customer
- **West India**: 2 customers

---

## 🧪 TESTING SCENARIOS

### **AI Chat Examples**

#### **Order Creation**
```
"Order 2 laptops for Rahul Sharma"
"Priya ko 3 mouse bhejo"
"Amit ke liye 1 monitor chahiye"
```

#### **Inventory Check**
```
"Check stock of Dell Laptop"
"Kitne keyboard available hai?"
"Mouse ka stock check karo"
```

#### **Invoice Generation**
```
"Generate invoice for order 1"
"Invoice chahiye order 5 ka"
"Create bill for Rahul's order"
```

#### **Customer Queries**
```
"Show orders for Priya Patel"
"Sneha Reddy ka pending order"
"List all customers from Mumbai"
```

---

## 📈 EXPECTED DASHBOARD STATS

After seeding data:
- **Total Revenue**: ₹2,00,000+
- **Total Orders**: 50
- **Total Customers**: 10
- **Total Products**: 20
- **Low Stock Items**: 2-5 products

---

## 🔧 CUSTOMIZATION

### **Add More Customers**
Edit `DEMO_CUSTOMERS` in `seed_demo_data.py`:
```python
{
    "name": "New Customer",
    "email": "email@example.com",
    "phone": "9XXXXXXXXX",
    "address": "Address here"
}
```

### **Add More Products**
Edit `DEMO_PRODUCTS`:
```python
{
    "name": "Product Name",
    "sku": "SKU-CODE",
    "price": 1000.00,
    "stock": 50,
    "category": "Category"
}
```

### **Change Order Count**
In `seed_demo_data.py`, line ~150:
```python
for i in range(50):  # Change 50 to desired number
```

---

## 🚀 RUNNING THE SEED SCRIPT

### **Step 1: Run Script**
```powershell
python seed_demo_data.py
```

### **Step 2: Expected Output**
```
============================================================
🚀 CREATING DEMO DATASET FOR INDIAN SMB
============================================================

CREATING CUSTOMERS
------------------------------------------------------------
✅ Created: Rahul Sharma (9876543210)
✅ Created: Priya Patel (9123456789)
...
📊 Total Customers: 10

CREATING PRODUCTS
------------------------------------------------------------
✅ Created: Dell Laptop i5 8GB (₹45,000.00) - Stock: 15
✅ Created: HP Laptop i7 16GB (₹65,000.00) - Stock: 10
...
📊 Total Products: 20

CREATING SAMPLE ORDERS
------------------------------------------------------------
✅ Created 10 orders...
✅ Created 20 orders...
...
📊 Total Orders: 50
💰 Total Revenue: ₹2,45,750.00

============================================================
📊 DEMO DATASET SUMMARY
============================================================
✅ Customers: 10
✅ Products: 20
✅ Orders: 50
💰 Total Revenue: ₹2,45,750.00
📦 Average Order Value: ₹4,915.00

🎉 DEMO DATASET CREATED SUCCESSFULLY!
```

---

## 📊 VERIFY DATA

### **Check Dashboard**
```
http://localhost:3000/dashboard.html
```

### **Test AI Agent**
```
http://localhost:3000
```

Try:
- "Show all customers"
- "Check stock of laptop"
- "Order 2 keyboards for Rahul"

---

## 🗑️ CLEAR DATA

To reset and start fresh:

### **Option 1: Python Script**
Uncomment the clear section in `seed_demo_data.py`:
```python
# Clear existing data
db.query(OrderItem).delete()
db.query(Order).delete()
db.query(Product).delete()
db.query(Customer).delete()
```

### **Option 2: SQL**
```sql
DELETE FROM order_items;
DELETE FROM orders;
DELETE FROM products;
DELETE FROM customers;
```

---

## 🎯 USE CASES

### **1. Demo/Presentation**
- Show realistic Indian SMB data
- Demonstrate AI chat capabilities
- Display dashboard metrics

### **2. Testing**
- Test order creation flow
- Verify inventory updates
- Check invoice generation

### **3. Development**
- Develop new features with realistic data
- Test edge cases
- Performance testing

---

## 📝 NOTES

- **Phone numbers**: All start with 9 (Indian mobile format)
- **Addresses**: Real Indian cities and localities
- **Pricing**: Realistic Indian market prices
- **Stock levels**: Varied to show low stock alerts
- **Order dates**: Distributed over 30 days for realistic timeline

---

**DEMO DATASET READY!** 🎉
