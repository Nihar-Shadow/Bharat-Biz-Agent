"""
Order API routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.order import OrderCreate, OrderResponse
from app.services.order_service import OrderService
from app.services.invoice_service import InvoiceService
from app.models.order import Order
from typing import List

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=OrderResponse, status_code=201)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    """
    Create a new order
    
    - **customer_id**: Customer ID (required)
    - **items**: List of order items (required, at least 1 item)
        - **product_id**: Product ID
        - **quantity**: Quantity ordered
    
    The endpoint will:
    - Validate stock availability
    - Calculate order total
    - Decrease product stock
    - Create order and order items
    - Log AI action
    """
    return OrderService.create_order(db, order)


@router.get("/", response_model=List[OrderResponse])
def get_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all orders with pagination
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100)
    """
    return OrderService.get_all_orders(db, skip, limit)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    """
    Get a specific order by ID with all items
    """
    order = OrderService.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.get("/customer/{customer_id}", response_model=List[OrderResponse])
def get_customer_orders(customer_id: int, db: Session = Depends(get_db)):
    """
    Get all orders for a specific customer
    """
    return OrderService.get_customer_orders(db, customer_id)


@router.post("/{order_id}/approve", response_model=OrderResponse)
def approve_order(order_id: int, db: Session = Depends(get_db)):
    """Approve order and generate invoice"""
    order = OrderService.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
        
    # Update status
    order.status = "approved"
    db.commit()
    db.refresh(order)
    
    # Generate Invoice
    InvoiceService.generate_invoice(db, order.id)
    
    return order

@router.post("/{order_id}/reject", response_model=OrderResponse)
def reject_order(order_id: int, db: Session = Depends(get_db)):
    """Reject order"""
    order = OrderService.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
        
    order.status = "rejected"
    db.commit()
    db.refresh(order)
    
    return order
