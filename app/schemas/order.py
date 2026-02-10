"""
Order Pydantic schemas
"""
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class OrderItemCreate(BaseModel):
    """Schema for creating an order item"""
    product_id: int = Field(..., gt=0, description="Product ID")
    quantity: int = Field(..., gt=0, description="Quantity ordered")


class OrderItemResponse(BaseModel):
    """Schema for order item response"""
    id: int
    product_id: int
    quantity: int
    price: float
    subtotal: float
    
    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    """Schema for creating an order"""
    customer_id: int = Field(..., gt=0, description="Customer ID")
    items: List[OrderItemCreate] = Field(..., min_length=1, description="Order items")


class OrderResponse(BaseModel):
    """Schema for order response"""
    id: int
    customer_id: int
    order_total: float
    status: str
    created_at: datetime
    items: List[OrderItemResponse]
    
    class Config:
        from_attributes = True
