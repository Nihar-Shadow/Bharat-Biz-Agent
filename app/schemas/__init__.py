"""
Pydantic schemas package
"""
from app.schemas.customer import CustomerCreate, CustomerResponse
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.schemas.order import OrderCreate, OrderItemCreate, OrderResponse
from app.schemas.invoice import InvoiceResponse
from app.schemas.dashboard import DashboardData

__all__ = [
    "CustomerCreate",
    "CustomerResponse",
    "ProductCreate",
    "ProductUpdate",
    "ProductResponse",
    "OrderCreate",
    "OrderItemCreate",
    "OrderResponse",
    "InvoiceResponse",
    "DashboardData"
]
