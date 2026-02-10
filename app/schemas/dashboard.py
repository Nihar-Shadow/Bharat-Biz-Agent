"""
Dashboard Pydantic schemas
"""
from pydantic import BaseModel
from typing import List
from app.schemas.product import ProductResponse


class DashboardData(BaseModel):
    """Schema for dashboard data"""
    total_customers: int
    total_products: int
    total_orders: int
    total_revenue: float
    low_stock_products: List[ProductResponse]
    recent_orders_count: int  # Orders in last 7 days
