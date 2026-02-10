"""
Order service - business logic for order operations
"""
from sqlalchemy.orm import Session
from app.models.order import Order, OrderItem
from app.schemas.order import OrderCreate
from app.services.product_service import ProductService
from app.services.ai_logger_service import AILoggerService
from typing import List, Optional
from fastapi import HTTPException


class OrderService:
    """Service class for order operations"""
    
    @staticmethod
    def create_order(db: Session, order_data: OrderCreate) -> Order:
        """Create a new order with items"""
        # Calculate total and validate stock
        order_total = 0.0
        order_items_data = []
        
        for item in order_data.items:
            product = ProductService.get_product(db, item.product_id)
            if not product:
                raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
            
            if product.stock_quantity < item.quantity:
                raise HTTPException(
                    status_code=400,
                    detail=f"Insufficient stock for product {product.name}. Available: {product.stock_quantity}"
                )
            
            item_total = product.price * item.quantity
            order_total += item_total
            
            order_items_data.append({
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price": product.price
            })
        
        # Create order
        order = Order(
            customer_id=order_data.customer_id,
            order_total=order_total
        )
        db.add(order)
        db.flush()  # Get order ID without committing
        
        # Create order items and decrease stock
        for item_data in order_items_data:
            order_item = OrderItem(
                order_id=order.id,
                **item_data
            )
            db.add(order_item)
            
            # Decrease stock
            ProductService.decrease_stock(db, item_data["product_id"], item_data["quantity"])
        
        db.commit()
        db.refresh(order)
        
        # Log AI action
        AILoggerService.log_action(
            db=db,
            action_type="ORDER_CREATED",
            input_text=f"Customer {order_data.customer_id} placed order",
            output_action=f"Order {order.id} created with total ${order_total:.2f}"
        )
        
        return order
    
    @staticmethod
    def get_order(db: Session, order_id: int) -> Optional[Order]:
        """Get order by ID with items"""
        return db.query(Order).filter(Order.id == order_id).first()
    
    @staticmethod
    def get_all_orders(db: Session, skip: int = 0, limit: int = 100) -> List[Order]:
        """Get all orders with pagination"""
        return db.query(Order).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_customer_orders(db: Session, customer_id: int) -> List[Order]:
        """Get all orders for a specific customer"""
        return db.query(Order).filter(Order.customer_id == customer_id).all()
