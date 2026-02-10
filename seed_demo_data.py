"""
Demo Dataset Seed Script for Indian SMB Business System
Generates realistic data: 20 products, 10 customers, 50 orders
"""
from datetime import datetime, timedelta
import random
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.customer import Customer
from app.models.product import Product
from app.models.order import Order, OrderItem


# Realistic Indian customer data (matching Customer model)
DEMO_CUSTOMERS = [
    {"name": "Rahul Sharma", "phone": "9876543210", "language_preference": "hi"},
    {"name": "Priya Patel", "phone": "9123456789", "language_preference": "en"},
    {"name": "Amit Kumar", "phone": "9988776655", "language_preference": "en"},
    {"name": "Sneha Reddy", "phone": "9876512345", "language_preference": "hi"},
    {"name": "Vikram Singh", "phone": "9765432109", "language_preference": "hi"},
    {"name": "Anjali Gupta", "phone": "9654321098", "language_preference": "en"},
    {"name": "Rajesh Verma", "phone": "9543210987", "language_preference": "hi"},
    {"name": "Kavita Joshi", "phone": "9432109876", "language_preference": "en"},
    {"name": "Suresh Nair", "phone": "9321098765", "language_preference": "en"},
    {"name": "Deepa Iyer", "phone": "9210987654", "language_preference": "en"}
]


# Realistic Indian SMB products (Electronics & Office Supplies)
# Matching Product model: name, price, stock_quantity, reorder_threshold
DEMO_PRODUCTS = [
    # Electronics
    {"name": "Dell Laptop i5 8GB", "price": 45000.00, "stock_quantity": 15, "reorder_threshold": 5},
    {"name": "HP Laptop i7 16GB", "price": 65000.00, "stock_quantity": 10, "reorder_threshold": 3},
    {"name": "Lenovo ThinkPad", "price": 55000.00, "stock_quantity": 12, "reorder_threshold": 4},
    {"name": "Logitech Wireless Mouse", "price": 500.00, "stock_quantity": 50, "reorder_threshold": 15},
    {"name": "Dell Wired Mouse", "price": 300.00, "stock_quantity": 75, "reorder_threshold": 20},
    {"name": "Mechanical Keyboard RGB", "price": 2500.00, "stock_quantity": 30, "reorder_threshold": 10},
    {"name": "Wireless Keyboard", "price": 1200.00, "stock_quantity": 40, "reorder_threshold": 12},
    {"name": "24-inch Dell Monitor", "price": 12000.00, "stock_quantity": 20, "reorder_threshold": 5},
    {"name": "27-inch LG Monitor", "price": 18000.00, "stock_quantity": 15, "reorder_threshold": 5},
    {"name": "1080p HD Webcam", "price": 2500.00, "stock_quantity": 25, "reorder_threshold": 8},
    {"name": "Noise Cancelling Headphones", "price": 3500.00, "stock_quantity": 35, "reorder_threshold": 10},
    {"name": "USB-C Hub 7-in-1", "price": 1800.00, "stock_quantity": 45, "reorder_threshold": 15},
    
    # Office Supplies
    {"name": "A4 Paper Ream (500 sheets)", "price": 250.00, "stock_quantity": 100, "reorder_threshold": 30},
    {"name": "Ballpoint Pen Box (50 pcs)", "price": 150.00, "stock_quantity": 80, "reorder_threshold": 25},
    {"name": "Stapler Heavy Duty", "price": 350.00, "stock_quantity": 60, "reorder_threshold": 15},
    {"name": "File Folders Pack (25)", "price": 400.00, "stock_quantity": 70, "reorder_threshold": 20},
    {"name": "Whiteboard Markers (12 pcs)", "price": 300.00, "stock_quantity": 55, "reorder_threshold": 18},
    {"name": "Desk Organizer", "price": 800.00, "stock_quantity": 40, "reorder_threshold": 10},
    {"name": "Calculator Scientific", "price": 600.00, "stock_quantity": 45, "reorder_threshold": 12},
    {"name": "Printer Ink Cartridge", "price": 1500.00, "stock_quantity": 30, "reorder_threshold": 10}
]


def create_demo_data():
    """Create demo dataset"""
    print("\n" + "="*60)
    print("🚀 CREATING DEMO DATASET FOR INDIAN SMB")
    print("="*60)
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Clear existing data (optional - comment out if you want to keep existing data)
        print("\n⚠️  Clearing existing data...")
        db.query(OrderItem).delete()
        db.query(Order).delete()
        db.query(Product).delete()
        db.query(Customer).delete()
        db.commit()
        print("✅ Existing data cleared")
        
        # Create customers
        print("\n" + "-"*60)
        print("CREATING CUSTOMERS")
        print("-"*60)
        
        customers = []
        for customer_data in DEMO_CUSTOMERS:
            customer = Customer(**customer_data)
            db.add(customer)
            customers.append(customer)
        
        db.commit()
        
        for customer in customers:
            db.refresh(customer)
            print(f"✅ Created: {customer.name} ({customer.phone})")
        
        print(f"\n📊 Total Customers: {len(customers)}")
        
        # Create products
        print("\n" + "-"*60)
        print("CREATING PRODUCTS")
        print("-"*60)
        
        products = []
        for product_data in DEMO_PRODUCTS:
            product = Product(**product_data)
            db.add(product)
            products.append(product)
        
        db.commit()
        
        for product in products:
            db.refresh(product)
            print(f"✅ Created: {product.name} (₹{product.price:,.2f}) - Stock: {product.stock_quantity}")
        
        print(f"\n📊 Total Products: {len(products)}")
        
        # Create orders
        print("\n" + "-"*60)
        print("CREATING SAMPLE ORDERS")
        print("-"*60)
        
        orders_created = 0
        total_revenue = 0
        
        # Generate 50 orders over the last 30 days
        for i in range(50):
            # Random customer
            customer = random.choice(customers)
            
            # Random date in last 30 days
            days_ago = random.randint(0, 30)
            order_date = datetime.now() - timedelta(days=days_ago)
            
            # Random status
            statuses = ["pending", "confirmed", "shipped", "delivered"]
            # Older orders more likely to be delivered
            if days_ago > 7:
                status = random.choice(["delivered", "delivered", "shipped"])
            else:
                status = random.choice(statuses)
            
            # Create order
            order = Order(
                customer_id=customer.id,
                status=status,
                total_amount=0,  # Will calculate
                created_at=order_date
            )
            db.add(order)
            db.flush()  # Get order ID
            
            # Add 1-4 random items to order
            num_items = random.randint(1, 4)
            order_total = 0
            
            selected_products = random.sample(products, num_items)
            
            for product in selected_products:
                # Random quantity (1-5)
                quantity = random.randint(1, 5)
                
                # Check stock
                if product.stock_quantity >= quantity:
                    unit_price = product.price
                    total_price = unit_price * quantity
                    
                    # Create order item
                    order_item = OrderItem(
                        order_id=order.id,
                        product_id=product.id,
                        quantity=quantity,
                        unit_price=unit_price,
                        total_price=total_price
                    )
                    db.add(order_item)
                    
                    # Update product stock
                    product.stock_quantity -= quantity
                    
                    order_total += total_price
            
            # Update order total
            order.total_amount = order_total
            total_revenue += order_total
            
            db.commit()
            db.refresh(order)
            
            orders_created += 1
            
            if orders_created % 10 == 0:
                print(f"✅ Created {orders_created} orders...")
        
        print(f"\n📊 Total Orders: {orders_created}")
        print(f"💰 Total Revenue: ₹{total_revenue:,.2f}")
        
        # Summary
        print("\n" + "="*60)
        print("📊 DEMO DATASET SUMMARY")
        print("="*60)
        print(f"✅ Customers: {len(customers)}")
        print(f"✅ Products: {len(products)}")
        print(f"✅ Orders: {orders_created}")
        print(f"💰 Total Revenue: ₹{total_revenue:,.2f}")
        print(f"📦 Average Order Value: ₹{total_revenue/orders_created:,.2f}")
        
        # Top customers by order count
        print("\n" + "-"*60)
        print("TOP 5 CUSTOMERS (by order count)")
        print("-"*60)
        
        from sqlalchemy import func
        top_customers = db.query(
            Customer.name,
            func.count(Order.id).label('order_count'),
            func.sum(Order.total_amount).label('total_spent')
        ).join(Order).group_by(Customer.id).order_by(func.count(Order.id).desc()).limit(5).all()
        
        for i, (name, order_count, total_spent) in enumerate(top_customers, 1):
            print(f"  {i}. {name}: {order_count} orders, ₹{total_spent:,.2f}")
        
        # Low stock products
        print("\n" + "-"*60)
        print("LOW STOCK ALERT (< 20 units)")
        print("-"*60)
        
        low_stock = db.query(Product).filter(Product.stock_quantity < 20).all()
        if low_stock:
            for product in low_stock:
                print(f"  ⚠️  {product.name}: {product.stock_quantity} units")
        else:
            print("  ✅ All products have sufficient stock")
        
        print("\n" + "="*60)
        print("🎉 DEMO DATASET CREATED SUCCESSFULLY!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error creating demo data: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("\n🔧 Initializing database...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized")
    
    create_demo_data()
    
    print("\n✅ Demo data creation complete!")
    print("\n📝 You can now:")
    print("   1. View data in dashboard: http://localhost:3000/dashboard.html")
    print("   2. Test AI agent with existing customers/products")
    print("   3. Generate invoices for orders")
    print("   4. Check inventory levels")
