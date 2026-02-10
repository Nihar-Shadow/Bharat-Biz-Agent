"""
Invoice database model
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Invoice(Base):
    """Invoice model"""
    
    __tablename__ = "invoices"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, unique=True, index=True)
    file_path = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Relationships
    order = relationship("Order", backref="invoice")
    
    def __repr__(self):
        return f"<Invoice(id={self.id}, order_id={self.order_id}, file='{self.file_path}')>"
