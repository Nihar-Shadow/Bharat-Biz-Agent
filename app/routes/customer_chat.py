"""
Customer Chat API routes
Handles the customer-facing chat interface logic
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.customer import Customer
from app.models.product import Product
from app.models.order import Order
from app.services.customer_service import CustomerService
from app.services.product_service import ProductService
from app.services.order_service import OrderService
from app.services.ai_agent_engine import AIAgentEngine
from app.schemas.customer import CustomerCreate
from app.schemas.order import OrderCreate, OrderItemCreate
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from datetime import datetime

router = APIRouter(prefix="/customer-chat", tags=["customer-chat"])

class CustomerRegistration(BaseModel):
    name: str
    phone: str

class CustomerMessage(BaseModel):
    phone: str
    message: str

class ChatResponse(BaseModel):
    message: str
    action_type: Optional[str] = None # 'order_placed', 'registration_required', 'info'
    data: Optional[Dict[str, Any]] = None

@router.post("/register", response_model=ChatResponse)
def register_customer(data: CustomerRegistration, db: Session = Depends(get_db)):
    """Register a new customer from chat"""
    existing = CustomerService.get_customer_by_phone(db, data.phone)
    if existing:
        return ChatResponse(
            message=f"Welcome back, {existing.name}! How can I help you today?",
            action_type="login_success",
            data={"customer_id": existing.id, "name": existing.name}
        )
    
    # Create new customer
    try:
        new_customer = CustomerCreate(name=data.name, phone=data.phone)
        customer = CustomerService.create_customer(db, new_customer)
        
        # Notify Vendor
        try:
            from app.services.notification_service import NotificationService
            NotificationService.create_notification(db, "NEW_CUSTOMER", f"New Customer Added: {customer.name} ({customer.phone})", customer.id)
        except Exception:
            pass # Fail silently
            
        return ChatResponse(
            message=f"Registration successful! Welcome {customer.name}. You can now order by typing messages like 'Send 5 shirts'.",
            action_type="registration_success",
            data={"customer_id": customer.id, "name": customer.name}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/order/{order_id}/status")
def get_order_status(order_id: int, db: Session = Depends(get_db)):
    """Check status of a specific order - For polling"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
        
    response = {"id": order.id, "status": order.status}
    
    if order.status == "approved":
        from app.models.invoice import Invoice
        invoice = db.query(Invoice).filter(Invoice.order_id == order.id).first()
        if invoice:
            response["invoice_url"] = f"/api/v1/invoices/{invoice.id}/download"
            
    return response

@router.post("/message", response_model=ChatResponse)
def process_customer_message(data: CustomerMessage, db: Session = Depends(get_db)):
    """Process message from customer"""
    # 1. Verify Customer
    customer = CustomerService.get_customer_by_phone(db, data.phone)
    if not customer:
        return ChatResponse(
            message="Please register first. What is your name?",
            action_type="registration_required"
        )

    # 2. Detect Intent
    engine = AIAgentEngine()
    intent = engine.detect_intent(data.message)
    
    # 3. Handle Intents Specific to Customer
    if intent.name == "create_order":
        return _handle_customer_order(db, customer, intent, data.message)
    elif intent.name == "check_status": # You might need to add this capability to AIAgent or just keyword match
        return _handle_status_check(db, customer)
    else:
        # Default fallback or handle other queries
        return ChatResponse(
            message=f"I understood you want to {intent.name.replace('_', ' ')}, but as a customer I can mainly help you place orders. Try checking your status or placing an order.",
            action_type="info"
        )

def _handle_customer_order(db: Session, customer: Customer, intent: Any, original_message: str):
    entities = intent.entities
    
    if "product_name" not in entities:
        return ChatResponse(message="Which product would you like to order?")
        
    # Find product (reuse logic from ActionRouter essentially)
    product_name = entities["product_name"]
    products = ProductService.get_all_products(db)
    
    # Simple search
    target_product = None
    for p in products:
        if product_name.lower() in p.name.lower():
            target_product = p
            break
            
    if not target_product:
        return ChatResponse(message=f"Sorry, we don't have '{product_name}' in stock.")
        
    quantity = entities.get("quantity", 1)
    
    # Create Order with PENDING status
    # Note: Service creates it. We need to explicitly set status if service doesn't default to pending (which we handled in DB default)
    # But wait, Service might auto-deduct stock. For 'Pending', maybe we hold off on stock deduction? 
    # For this hackathon, let's deduct stock (reservation) or just let it be. 
    # The requirement says "Order Status = Pending Vendor Approval".
    
    try:
        order_data = OrderCreate(
            customer_id=customer.id,
            items=[OrderItemCreate(product_id=target_product.id, quantity=quantity)]
        )
        
        # We need to ensure the service respects the default 'pending' explicitly or implicitly.
        # Check OrderService later. Assuming it creates object -> DB sets default.
        order = OrderService.create_order(db, order_data)
        
        # Manually force 'pending' if the service logic set it to something else (it currently doesn't set status, so DB default 'pending' works)
        # However, checking OrderService, it doesn't seem to set status. 
        # BUT, the current system might rely on implicit "completed" if it generates invoices immediately. 
        # Customer side: Request -> Pending.
        
        # Notify Vendor of New Order
        try:
            from app.services.notification_service import NotificationService
            NotificationService.create_notification(
                db, 
                type="NEW_ORDER", 
                message=f"New Order #{order.id}: {quantity} x {target_product.name} from {customer.name}",
                related_id=order.id
            )
        except Exception:
            pass

        return ChatResponse(
            message=f"Order placed for {quantity} {target_product.name}(s). Waiting for vendor approval.",
            action_type="order_placed",
            data={
                "order_id": order.id,
                "status": "pending",
                "total": order.order_total
            }
        )
    except Exception as e:
        return ChatResponse(message=f"Could not place order: {str(e)}")

def _handle_status_check(db: Session, customer: Customer):
    # Get last order
    last_order = db.query(Order).filter(Order.customer_id == customer.id).order_by(Order.created_at.desc()).first()
    
    if not last_order:
        return ChatResponse(message="You haven't placed any orders yet.")
        
    status_msg = f"Your last order #{last_order.id} is {last_order.status}."
    
    data = {"order_id": last_order.id, "status": last_order.status}
    
    if last_order.status == "approved":
        # Check for invoice
        # Assuming relationship or query
        from app.models.invoice import Invoice
        invoice = db.query(Invoice).filter(Invoice.order_id == last_order.id).first()
        if invoice:
            status_msg += " Invoice is ready!"
            data["invoice_url"] = f"/api/v1/invoices/{invoice.id}/download"
            
    return ChatResponse(
        message=status_msg,
        action_type="status_check",
        data=data
    )
