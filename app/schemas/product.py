"""
Product Pydantic schemas
"""
from pydantic import BaseModel, Field
from typing import Optional


class ProductCreate(BaseModel):
    """Schema for creating a product"""
    name: str = Field(..., min_length=1, max_length=255, description="Product name")
    price: float = Field(..., gt=0, description="Product price")
    stock_quantity: int = Field(default=0, ge=0, description="Current stock quantity")
    reorder_threshold: int = Field(default=10, ge=0, description="Reorder threshold")


class ProductUpdate(BaseModel):
    """Schema for updating product"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    price: Optional[float] = Field(None, gt=0)
    stock_quantity: Optional[int] = Field(None, ge=0)
    reorder_threshold: Optional[int] = Field(None, ge=0)


class ProductResponse(BaseModel):
    """Schema for product response"""
    id: int
    name: str
    price: float
    stock_quantity: int
    reorder_threshold: int
    needs_reorder: bool
    
    class Config:
        from_attributes = True
