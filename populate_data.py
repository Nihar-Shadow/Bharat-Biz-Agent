"""
Quick Database Population Script
Adds sample customers and products so you can immediately test the chat interface
"""
import requests
import sys

BASE_URL = "http://localhost:8000/api/v1"

def populate_database():
    """Populate database with sample data"""
    
    print("🚀 Populating Database with Sample Data\n")
    print("="*60)
    
    # Check if backend is running
    try:
        r = requests.get("http://localhost:8000/health")
        if r.status_code != 200:
            print("❌ Backend is not healthy")
            return False
    except:
        print("❌ Cannot connect to backend at http://localhost:8000")
        print("Make sure the backend is running:")
        print("   python -m uvicorn app.main:app --reload")
        return False
    
    print("✅ Backend is running\n")
    
    # Add customers
    print("👥 Adding Customers...")
    customers = [
        {"name": "Alice", "phone": "+919876543210", "language_preference": "en"},
        {"name": "Bob", "phone": "+919123456789", "language_preference": "en"},
        {"name": "Charlie", "phone": "+919999888877", "language_preference": "en"},
        {"name": "Rahul", "phone": "+919555666777", "language_preference": "hi"},
        {"name": "Priya", "phone": "+919444333222", "language_preference": "en"}
    ]
    
    added_customers = 0
    for customer in customers:
        try:
            r = requests.post(f"{BASE_URL}/customers/", json=customer)
            if r.status_code == 201:
                data = r.json()
                print(f"   ✅ {data['name']} (ID: {data['id']}, Phone: {data['phone']})")
                added_customers += 1
            elif r.status_code == 400 and "already registered" in r.json().get("detail", ""):
                print(f"   ⚠️  {customer['name']} already exists")
            else:
                print(f"   ❌ Failed to add {customer['name']}: {r.json()}")
        except Exception as e:
            print(f"   ❌ Error adding {customer['name']}: {e}")
    
    print(f"\n   Total customers added: {added_customers}")
    
    # Add products
    print("\n📦 Adding Products...")
    products = [
        {"name": "Laptop", "price": 1299.99, "stock_quantity": 25, "reorder_threshold": 5},
        {"name": "Mouse", "price": 29.99, "stock_quantity": 50, "reorder_threshold": 10},
        {"name": "Keyboard", "price": 79.99, "stock_quantity": 30, "reorder_threshold": 8},
        {"name": "Cable", "price": 9.99, "stock_quantity": 100, "reorder_threshold": 20},
        {"name": "Headphones", "price": 149.99, "stock_quantity": 15, "reorder_threshold": 5}
    ]
    
    added_products = 0
    for product in products:
        try:
            r = requests.post(f"{BASE_URL}/products/", json=product)
            if r.status_code == 201:
                data = r.json()
                print(f"   ✅ {data['name']} (ID: {data['id']}, Stock: {data['stock_quantity']}, Price: ₹{data['price']})")
                added_products += 1
            else:
                print(f"   ⚠️  {product['name']} may already exist")
        except Exception as e:
            print(f"   ❌ Error adding {product['name']}: {e}")
    
    print(f"\n   Total products added: {added_products}")
    
    print("\n" + "="*60)
    print("✅ Database Population Complete!\n")
    
    # Show what to do next
    print("🎯 Now you can try these messages in the chat interface:\n")
    print("   📝 Create Order:")
    print("      'Order 2 laptops for Alice'")
    print("      'Order 3 mice for Bob'")
    print("      'Laptop chahiye 2 pieces for Rahul'\n")
    
    print("   📊 Check Inventory:")
    print("      'Check stock of laptop'")
    print("      'Mouse kitne available hai?'\n")
    
    print("   📄 Generate Invoice:")
    print("      'Generate invoice for order 1'\n")
    
    print("🌐 Open chat interface: http://localhost:3000")
    print("📖 API Docs: http://localhost:8000/docs\n")
    
    return True

if __name__ == "__main__":
    try:
        success = populate_database()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
