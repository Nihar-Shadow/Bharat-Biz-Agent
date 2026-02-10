"""
Customer Pydantic schemas
"""
from pydantic import BaseModel, Field


class CustomerCreate(BaseModel):
    """Schema for creating a customer"""
    name: str = Field(..., min_length=1, max_length=255, description="Customer name")
    phone: str = Field(..., min_length=10, max_length=20, description="Customer phone number")
    language_preference: str = Field(default="en", max_length=10, description="Preferred language code")


class CustomerResponse(BaseModel):
    """Schema for customer response"""
    id: int
    name: str
    phone: str
    language_preference: str
    
    class Config:
        from_attributes = True
