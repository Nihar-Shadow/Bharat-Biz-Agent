"""
Customer database model
"""
from sqlalchemy import Column, Integer, String
from app.database import Base


class Customer(Base):
    """Customer model"""
    
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False, index=True)
    phone = Column(String(20), nullable=False, unique=True, index=True)
    language_preference = Column(String(10), default="en", nullable=False)
    
    def __repr__(self):
        return f"<Customer(id={self.id}, name='{self.name}', phone='{self.phone}')>"
