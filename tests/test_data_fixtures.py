"""
Test Data Fixtures for Integration Tests
Sample data for various test scenarios
"""

# Sample chat messages for testing
CHAT_TEST_MESSAGES = {
    "create_order_english": [
        "Order 2 laptops for Rahul Kumar",
        "I need 5 keyboards for Priya",
        "Place order: 3 mouse, 2 keyboards for Amit",
    ],
    
    "create_order_hindi": [
        "Rahul ke liye 2 laptop chahiye",
        "Mujhe 3 keyboard chahiye",
    ],
    
    "create_order_hinglish": [
        "2 laptop order karo Rahul ke liye",
        "Priya ko 5 mouse bhejo",
    ],
    
    "check_inventory": [
        "Check stock of laptop",
        "How many keyboards available?",
        "Kitne mouse hai stock mein?",
        "Laptop ka stock check karo",
    ],
    
    "generate_invoice": [
        "Generate invoice for order 1",
        "Create bill for order #5",
        "Invoice chahiye order 3 ka",
    ],
    
    "add_customer": [
        "Add customer Rahul phone 9876543210",
        "New customer: Priya, email priya@test.com",
        "Customer add karo: Amit, 9123456789",
    ],
    
    "payment_reminder": [
        "Send payment reminder to Rahul",
        "Remind Priya about pending payment",
        "Payment reminder bhejo Amit ko",
    ]
}


# Sample customer data
SAMPLE_CUSTOMERS = [
    {
        "name": "Rahul Kumar",
        "email": "rahul@test.com",
        "phone": "9876543210",
        "address": "123 MG Road, Mumbai, Maharashtra 400001"
    },
    {
        "name": "Priya Sharma",
        "email": "priya@test.com",
        "phone": "9123456789",
        "address": "456 Park Street, Delhi, Delhi 110001"
    },
    {
        "name": "Amit Patel",
        "email": "amit@test.com",
        "phone": "9988776655",
        "address": "789 Brigade Road, Bangalore, Karnataka 560001"
    },
    {
        "name": "Sneha Reddy",
        "email": "sneha@test.com",
        "phone": "9876512345",
        "address": "321 Banjara Hills, Hyderabad, Telangana 500034"
    }
]


# Sample product data
SAMPLE_PRODUCTS = [
    {
        "name": "Laptop",
        "sku": "LAP001",
        "price": 45000.00,
        "stock_quantity": 10,
        "description": "Dell Inspiron 15, 8GB RAM, 512GB SSD"
    },
    {
        "name": "Mouse",
        "sku": "MOU001",
        "price": 500.00,
        "stock_quantity": 50,
        "description": "Logitech Wireless Mouse"
    },
    {
        "name": "Keyboard",
        "sku": "KEY001",
        "price": 1500.00,
        "stock_quantity": 30,
        "description": "Mechanical Keyboard RGB"
    },
    {
        "name": "Monitor",
        "sku": "MON001",
        "price": 12000.00,
        "stock_quantity": 15,
        "description": "24-inch Full HD Monitor"
    },
    {
        "name": "Webcam",
        "sku": "WEB001",
        "price": 2500.00,
        "stock_quantity": 20,
        "description": "1080p HD Webcam"
    },
    {
        "name": "Headphones",
        "sku": "HEAD001",
        "price": 3000.00,
        "stock_quantity": 25,
        "description": "Noise Cancelling Headphones"
    }
]


# Sample order scenarios
ORDER_SCENARIOS = [
    {
        "name": "Simple Single Item Order",
        "message": "Order 2 laptops for Rahul Kumar",
        "expected_items": [
            {"product": "Laptop", "quantity": 2}
        ],
        "expected_total": 90000.00
    },
    {
        "name": "Multiple Items Order",
        "message": "Order 3 keyboards and 5 mouse for Priya",
        "expected_items": [
            {"product": "Keyboard", "quantity": 3},
            {"product": "Mouse", "quantity": 5}
        ],
        "expected_total": 7000.00
    },
    {
        "name": "Hindi Order",
        "message": "Amit ke liye 1 monitor aur 2 headphones chahiye",
        "expected_items": [
            {"product": "Monitor", "quantity": 1},
            {"product": "Headphones", "quantity": 2}
        ],
        "expected_total": 18000.00
    }
]


# Expected AI responses for validation
EXPECTED_AI_RESPONSES = {
    "create_order": {
        "intent": "create_order",
        "min_confidence": 0.7,
        "required_entities": ["customer_name", "product_name", "quantity"]
    },
    "check_inventory": {
        "intent": "check_inventory",
        "min_confidence": 0.7,
        "required_entities": ["product_name"]
    },
    "generate_invoice": {
        "intent": "generate_invoice",
        "min_confidence": 0.7,
        "required_entities": ["order_id"]
    },
    "add_customer": {
        "intent": "add_customer",
        "min_confidence": 0.7,
        "required_entities": ["customer_name"]
    }
}


# Database validation rules
DB_VALIDATION_RULES = {
    "order": {
        "required_fields": ["id", "customer_id", "total_amount", "status", "created_at"],
        "status_values": ["pending", "confirmed", "shipped", "delivered", "cancelled"],
        "min_total_amount": 0.01
    },
    "order_item": {
        "required_fields": ["id", "order_id", "product_id", "quantity", "unit_price", "total_price"],
        "min_quantity": 1,
        "min_price": 0.01
    },
    "customer": {
        "required_fields": ["id", "name", "created_at"],
        "optional_fields": ["email", "phone", "address"]
    },
    "product": {
        "required_fields": ["id", "name", "sku", "price", "stock_quantity"],
        "min_price": 0.01,
        "min_stock": 0
    },
    "ai_action_log": {
        "required_fields": ["id", "intent", "confidence", "success", "created_at"],
        "min_confidence": 0.0,
        "max_confidence": 1.0
    }
}


# File validation rules
FILE_VALIDATION_RULES = {
    "invoice": {
        "directory": "invoices",
        "file_pattern": r"invoice_\d+_\d+\.pdf",
        "min_size_bytes": 100,
        "max_size_bytes": 10 * 1024 * 1024  # 10MB
    }
}


# Dashboard expected metrics
DASHBOARD_METRICS = {
    "total_revenue": {
        "type": "float",
        "min_value": 0.0
    },
    "total_orders": {
        "type": "int",
        "min_value": 0
    },
    "total_customers": {
        "type": "int",
        "min_value": 0
    },
    "low_stock_count": {
        "type": "int",
        "min_value": 0
    }
}


# Test configuration
TEST_CONFIG = {
    "database": {
        "url": "sqlite:///./test_integration.db",
        "echo": False
    },
    "api": {
        "base_url": "http://localhost:8000",
        "timeout": 30
    },
    "cleanup": {
        "delete_test_db": True,
        "delete_test_invoices": True
    },
    "logging": {
        "level": "INFO",
        "file": "test_integration.log"
    }
}


# Error scenarios for negative testing
ERROR_SCENARIOS = [
    {
        "name": "Invalid Product",
        "message": "Order 5 nonexistent_product for Rahul",
        "expected_error": "Product not found"
    },
    {
        "name": "Insufficient Stock",
        "message": "Order 100 laptops for Priya",  # More than available
        "expected_error": "Insufficient stock"
    },
    {
        "name": "Invalid Customer",
        "message": "Order 2 mouse for NonExistentCustomer",
        "expected_behavior": "create_customer_or_fail"
    },
    {
        "name": "Ambiguous Message",
        "message": "I want something",
        "expected_intent": "unknown"
    }
]


# Performance benchmarks
PERFORMANCE_BENCHMARKS = {
    "ai_processing": {
        "max_time_seconds": 2.0,
        "description": "AI intent detection and entity extraction"
    },
    "order_creation": {
        "max_time_seconds": 1.0,
        "description": "Database order insertion"
    },
    "invoice_generation": {
        "max_time_seconds": 3.0,
        "description": "PDF invoice file generation"
    },
    "dashboard_query": {
        "max_time_seconds": 0.5,
        "description": "Dashboard metrics calculation"
    }
}
