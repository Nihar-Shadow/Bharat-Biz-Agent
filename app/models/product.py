"""
Product database model
"""
from sqlalchemy import Column, Integer, String, Float
from app.database import Base


class Product(Base):
    """Product model"""
    
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False, index=True)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, default=0, nullable=False)
    reorder_threshold = Column(Integer, default=10, nullable=False)
    
    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', stock={self.stock_quantity})>"
    
    @property
    def needs_reorder(self) -> bool:
        """Check if product needs reordering"""
        return self.stock_quantity <= self.reorder_threshold
