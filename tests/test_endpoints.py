"""
Test endpoints - Sample test cases for the API
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, get_db
from sqlalchemy.orm import sessionmaker

# Create test database
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["status"] == "running"


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_customer():
    """Test creating a customer"""
    customer_data = {
        "name": "Test Customer",
        "phone": "+1234567890",
        "language_preference": "en"
    }
    response = client.post("/api/v1/customers/", json=customer_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == customer_data["name"]
    assert data["phone"] == customer_data["phone"]
    assert "id" in data


def test_create_product():
    """Test creating a product"""
    product_data = {
        "name": "Test Product",
        "price": 99.99,
        "stock_quantity": 100,
        "reorder_threshold": 20
    }
    response = client.post("/api/v1/products/", json=product_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == product_data["name"]
    assert data["price"] == product_data["price"]
    assert "id" in data


def test_get_dashboard():
    """Test dashboard endpoint"""
    response = client.get("/api/v1/dashboard/")
    assert response.status_code == 200
    data = response.json()
    assert "total_customers" in data
    assert "total_products" in data
    assert "total_orders" in data
    assert "total_revenue" in data
    assert "low_stock_products" in data


def test_create_order():
    """Test creating an order (requires existing customer and product)"""
    # First create a customer
    customer_data = {
        "name": "Order Test Customer",
        "phone": "+9876543210",
        "language_preference": "en"
    }
    customer_response = client.post("/api/v1/customers/", json=customer_data)
    customer_id = customer_response.json()["id"]
    
    # Create a product
    product_data = {
        "name": "Order Test Product",
        "price": 50.00,
        "stock_quantity": 50,
        "reorder_threshold": 10
    }
    product_response = client.post("/api/v1/products/", json=product_data)
    product_id = product_response.json()["id"]
    
    # Create order
    order_data = {
        "customer_id": customer_id,
        "items": [
            {
                "product_id": product_id,
                "quantity": 2
            }
        ]
    }
    response = client.post("/api/v1/orders/", json=order_data)
    assert response.status_code == 201
    data = response.json()
    assert data["customer_id"] == customer_id
    assert data["order_total"] == 100.00
    assert len(data["items"]) == 1


def test_generate_invoice():
    """Test invoice generation (requires existing order)"""
    # Create customer, product, and order first
    customer_data = {
        "name": "Invoice Test Customer",
        "phone": "+1122334455",
        "language_preference": "en"
    }
    customer_response = client.post("/api/v1/customers/", json=customer_data)
    customer_id = customer_response.json()["id"]
    
    product_data = {
        "name": "Invoice Test Product",
        "price": 75.00,
        "stock_quantity": 30,
        "reorder_threshold": 5
    }
    product_response = client.post("/api/v1/products/", json=product_data)
    product_id = product_response.json()["id"]
    
    order_data = {
        "customer_id": customer_id,
        "items": [{"product_id": product_id, "quantity": 1}]
    }
    order_response = client.post("/api/v1/orders/", json=order_data)
    order_id = order_response.json()["id"]
    
    # Generate invoice
    response = client.post(f"/api/v1/invoices/generate/{order_id}")
    assert response.status_code == 201
    data = response.json()
    assert data["order_id"] == order_id
    assert "file_path" in data
    assert "id" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
