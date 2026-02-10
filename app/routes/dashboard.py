"""
Dashboard API routes
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.schemas.dashboard import DashboardData
from app.models.customer import Customer
from app.models.product import Product
from app.models.order import Order
from app.services.product_service import ProductService
from datetime import datetime, timedelta

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/", response_model=DashboardData)
def get_dashboard_data(db: Session = Depends(get_db)):
    """
    Get aggregated dashboard data
    
    Returns:
    - Total number of customers
    - Total number of products
    - Total number of orders
    - Total revenue (sum of all orders)
    - List of low stock products
    - Number of recent orders (last 7 days)
    """
    # Count totals
    total_customers = db.query(func.count(Customer.id)).scalar()
    total_products = db.query(func.count(Product.id)).scalar()
    total_orders = db.query(func.count(Order.id)).scalar()
    
    # Calculate total revenue
    total_revenue = db.query(func.sum(Order.order_total)).scalar() or 0.0
    
    # Get low stock products
    low_stock_products = ProductService.get_low_stock_products(db)
    
    # Count recent orders (last 7 days)
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    recent_orders_count = db.query(func.count(Order.id)).filter(
        Order.created_at >= seven_days_ago
    ).scalar()
    
    return DashboardData(
        total_customers=total_customers,
        total_products=total_products,
        total_orders=total_orders,
        total_revenue=total_revenue,
        low_stock_products=low_stock_products,
        recent_orders_count=recent_orders_count
    )
