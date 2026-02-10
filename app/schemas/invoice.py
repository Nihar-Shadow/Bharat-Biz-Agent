"""
Invoice Pydantic schemas
"""
from pydantic import BaseModel
from datetime import datetime


class InvoiceResponse(BaseModel):
    """Schema for invoice response"""
    id: int
    order_id: int
    file_path: str
    created_at: datetime
    
    class Config:
        from_attributes = True
