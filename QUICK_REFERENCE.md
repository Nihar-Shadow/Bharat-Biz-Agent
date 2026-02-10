# 🎯 SMB Business Automation Backend - Quick Reference

## 📦 Project Overview

A production-ready FastAPI backend for AI-powered SMB business automation with:
- ✅ Customer Management
- ✅ Product Inventory with Auto-Reorder Alerts
- ✅ Order Processing with Stock Validation
- ✅ PDF Invoice Generation
- ✅ AI Action Logging
- ✅ Real-time Dashboard Analytics

## 🚀 Quick Start Commands

### Start Server
```bash
# Option 1: Using the start script
python start.py

# Option 2: Direct uvicorn
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Option 3: Using Docker
docker-compose up --build
```

### Test API
```bash
# Run comprehensive test script
python test_api.py

# Run unit tests
pytest tests/ -v
```

## 📡 API Endpoints Reference

### Base URL: `http://localhost:8000/api/v1`

#### 🧑 Customers
```bash
# Create Customer
POST /customers/
Body: {"name": "John Doe", "phone": "+1234567890", "language_preference": "en"}

# List Customers
GET /customers/?skip=0&limit=100

# Get Customer
GET /customers/{id}
```

#### 📦 Products
```bash
# Create Product
POST /products/
Body: {"name": "Laptop", "price": 999.99, "stock_quantity": 50, "reorder_threshold": 10}

# List Products
GET /products/?skip=0&limit=100

# Get Product
GET /products/{id}

# Update Inventory
PATCH /products/{id}/inventory
Body: {"stock_quantity": 100}

# Get Low Stock Products
GET /products/low-stock
```

#### 🛒 Orders
```bash
# Create Order
POST /orders/
Body: {
  "customer_id": 1,
  "items": [
    {"product_id": 1, "quantity": 2},
    {"product_id": 2, "quantity": 1}
  ]
}

# List Orders
GET /orders/?skip=0&limit=100

# Get Order
GET /orders/{id}

# Get Customer Orders
GET /orders/customer/{customer_id}
```

#### 🧾 Invoices
```bash
# Generate Invoice
POST /invoices/generate/{order_id}

# Get Invoice
GET /invoices/{id}

# Download PDF
GET /invoices/{id}/download

# Get Invoice by Order
GET /invoices/order/{order_id}
```

#### 📊 Dashboard
```bash
# Get Dashboard Metrics
GET /dashboard/
```

## 🗄️ Database Schema

```
Customers
├── id (PK)
├── name
├── phone (Unique)
└── language_preference

Products
├── id (PK)
├── name
├── price
├── stock_quantity
└── reorder_threshold

Orders
├── id (PK)
├── customer_id (FK → Customers)
├── order_total
└── created_at

Order_Items
├── id (PK)
├── order_id (FK → Orders)
├── product_id (FK → Products)
├── quantity
└── price

Invoices
├── id (PK)
├── order_id (FK → Orders, Unique)
├── file_path
└── created_at

AI_Actions_Log
├── id (PK)
├── action_type
├── input_text
├── output_action
└── timestamp
```

## 📂 Project Structure

```
c:\Nurothon\
├── app/
│   ├── models/              # SQLAlchemy database models
│   │   ├── customer.py      # Customer model
│   │   ├── product.py       # Product model with reorder logic
│   │   ├── order.py         # Order & OrderItem models
│   │   ├── invoice.py       # Invoice model
│   │   └── ai_action.py     # AI action logging model
│   │
│   ├── schemas/             # Pydantic validation schemas
│   │   ├── customer.py      # Customer request/response schemas
│   │   ├── product.py       # Product schemas
│   │   ├── order.py         # Order schemas with nested items
│   │   ├── invoice.py       # Invoice schemas
│   │   └── dashboard.py     # Dashboard data schema
│   │
│   ├── services/            # Business logic layer
│   │   ├── customer_service.py      # Customer CRUD operations
│   │   ├── product_service.py       # Product & inventory management
│   │   ├── order_service.py         # Order processing with validation
│   │   ├── invoice_service.py       # PDF invoice generation
│   │   └── ai_logger_service.py     # AI action logging
│   │
│   ├── routes/              # API endpoint definitions
│   │   ├── customers.py     # Customer endpoints
│   │   ├── products.py      # Product endpoints
│   │   ├── orders.py        # Order endpoints
│   │   ├── invoices.py      # Invoice endpoints
│   │   └── dashboard.py     # Dashboard endpoint
│   │
│   ├── config.py            # Application configuration
│   ├── database.py          # Database setup & session management
│   └── main.py              # FastAPI app initialization
│
├── invoices/                # Generated PDF invoices (auto-created)
├── tests/
│   └── test_endpoints.py    # Comprehensive API tests
│
├── Dockerfile               # Docker container definition
├── docker-compose.yml       # Docker Compose orchestration
├── requirements.txt         # Python dependencies
├── start.py                 # Quick start script
├── test_api.py              # API demonstration script
├── .env.example             # Environment variables template
├── .gitignore               # Git ignore rules
└── README.md                # Full documentation
```

## 🔑 Key Features Explained

### 1. Automatic Inventory Management
- Stock decreases automatically when orders are created
- Low stock alerts via `/products/low-stock` endpoint
- Reorder threshold tracking per product

### 2. Order Validation
- Validates customer exists
- Checks product availability
- Prevents overselling (stock validation)
- Calculates totals automatically

### 3. PDF Invoice Generation
- Professional invoice layout using ReportLab
- Includes customer details, itemized products, totals
- Stored in `invoices/` directory
- Downloadable via API

### 4. AI Action Logging
- Tracks all automated actions
- Searchable by action type
- Timestamp tracking for analytics
- Useful for audit trails

### 5. Dashboard Analytics
- Total customers, products, orders
- Revenue tracking
- Recent orders (last 7 days)
- Low stock product alerts

## 🧪 Testing

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test
```bash
pytest tests/test_endpoints.py::test_create_customer -v
```

### Manual API Testing
```bash
# Test with the demo script
python test_api.py

# Or use the interactive docs
# Open: http://localhost:8000/docs
```

## 🐳 Docker Deployment

### Build and Run
```bash
docker-compose up --build
```

### Stop
```bash
docker-compose down
```

### View Logs
```bash
docker-compose logs -f
```

## 🔧 Configuration

Edit `app/config.py` for:
- Database URL
- Invoice directory path
- API version prefix
- Debug mode

## 📊 Sample Workflow

1. **Create Customer**
   ```bash
   POST /api/v1/customers/
   ```

2. **Add Products**
   ```bash
   POST /api/v1/products/
   ```

3. **Create Order**
   ```bash
   POST /api/v1/orders/
   # Automatically validates stock and updates inventory
   ```

4. **Generate Invoice**
   ```bash
   POST /api/v1/invoices/generate/{order_id}
   # Creates PDF invoice
   ```

5. **Check Dashboard**
   ```bash
   GET /api/v1/dashboard/
   # View all metrics
   ```

## 🌐 Access Points

- **API**: http://localhost:8000
- **Interactive Docs (Swagger)**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 💡 Tips

1. **Use Interactive Docs**: The `/docs` endpoint provides a full UI to test all endpoints
2. **Check Logs**: AI actions are logged automatically for debugging
3. **Low Stock Alerts**: Monitor `/products/low-stock` for inventory management
4. **Invoice Storage**: PDFs are saved in `invoices/` directory
5. **Database**: SQLite file `smb_business.db` is created automatically

## 🚨 Common Issues

### Port Already in Use
```bash
# Find and kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Module Not Found
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Database Locked
```bash
# Stop server and delete database
rm smb_business.db
# Restart server (database will be recreated)
```

## 📈 Production Checklist

- [ ] Migrate to PostgreSQL/MySQL
- [ ] Add authentication (JWT/OAuth2)
- [ ] Configure CORS for specific origins
- [ ] Add rate limiting
- [ ] Set up logging infrastructure
- [ ] Add monitoring (Prometheus/Grafana)
- [ ] Use environment variables for secrets
- [ ] Set DEBUG=False
- [ ] Add backup strategy
- [ ] Configure SSL/TLS

## 🎓 Architecture Highlights

### Separation of Concerns
- **Models**: Database schema (SQLAlchemy)
- **Schemas**: Request/response validation (Pydantic)
- **Services**: Business logic
- **Routes**: API endpoints

### Design Patterns
- Repository pattern (Services layer)
- Dependency injection (FastAPI Depends)
- Factory pattern (Database session)

### Best Practices
- Type hints throughout
- Comprehensive error handling
- Input validation
- Modular structure
- Docker-ready
- Test coverage

---

**Built for hackathons and production-ready SMB automation** 🚀
