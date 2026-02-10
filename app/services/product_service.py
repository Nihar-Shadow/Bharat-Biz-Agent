"""
Product service - business logic for product operations
"""
from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from typing import List, Optional


class ProductService:
    """Service class for product operations"""
    
    @staticmethod
    def create_product(db: Session, product_data: ProductCreate) -> Product:
        """Create a new product"""
        product = Product(
            name=product_data.name,
            price=product_data.price,
            stock_quantity=product_data.stock_quantity,
            reorder_threshold=product_data.reorder_threshold
        )
        db.add(product)
        db.commit()
        db.refresh(product)
        return product
    
    @staticmethod
    def get_product(db: Session, product_id: int) -> Optional[Product]:
        """Get product by ID"""
        return db.query(Product).filter(Product.id == product_id).first()
    
    @staticmethod
    def get_all_products(db: Session, skip: int = 0, limit: int = 100) -> List[Product]:
        """Get all products with pagination"""
        return db.query(Product).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_product(db: Session, product_id: int, update_data: ProductUpdate) -> Optional[Product]:
        """Update existing product"""
        product = db.query(Product).filter(Product.id == product_id).first()
        if product:
            if update_data.name is not None:
                product.name = update_data.name
            if update_data.price is not None:
                product.price = update_data.price
            if update_data.stock_quantity is not None:
                product.stock_quantity = update_data.stock_quantity
            if update_data.reorder_threshold is not None:
                product.reorder_threshold = update_data.reorder_threshold
            
            db.commit()
            db.refresh(product)
        return product
    
    @staticmethod
    def delete_product(db: Session, product_id: int) -> bool:
        """Delete a product"""
        product = db.query(Product).filter(Product.id == product_id).first()
        if product:
            db.delete(product)
            db.commit()
            return True
        return False
    
    @staticmethod
    def get_low_stock_products(db: Session) -> List[Product]:
        """Get products that need reordering"""
        return db.query(Product).filter(
            Product.stock_quantity <= Product.reorder_threshold
        ).all()
    
    @staticmethod
    def decrease_stock(db: Session, product_id: int, quantity: int) -> bool:
        """Decrease stock quantity (for order processing)"""
        product = db.query(Product).filter(Product.id == product_id).first()
        if product and product.stock_quantity >= quantity:
            product.stock_quantity -= quantity
            db.commit()
            
            # Check for Low Stock
            if product.stock_quantity <= product.reorder_threshold:
                ProductService._trigger_low_stock_alert(db, product)
                
            return True
        return False

    @staticmethod
    def _trigger_low_stock_alert(db: Session, product: Product):
        """Trigger low stock notification with spam prevention"""
        from app.services.notification_service import NotificationService
        from app.models.notification import Notification
        from datetime import datetime, timedelta
        
        # Check spam (1 hour cooldown)
        # Note: We use the Notification table itself to track last alert
        one_hour_ago = datetime.utcnow() - timedelta(hours=1)
        recent_alert = db.query(Notification).filter(
            Notification.type == "LOW_STOCK",
            Notification.related_id == product.id,
            Notification.created_at >= one_hour_ago
        ).first()
        
        if not recent_alert:
            msg = f"Product: {product.name}\nRemaining Stock: {product.stock_quantity}\nMinimum Required: {product.reorder_threshold}"
            NotificationService.create_notification(
                db, 
                "LOW_STOCK", 
                msg,
                product.id
            )
