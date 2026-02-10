from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.customer import Customer
from app.services.customer_service import CustomerService
from pydantic import BaseModel
from typing import Dict, Any, Optional

router = APIRouter(prefix="/chat-onboarding", tags=["chat-onboarding"])

class ChatRequest(BaseModel):
    session_id: str
    message: str | None = None
    state: str = "NEW_USER"  # NEW_USER, ASK_NAME, ASK_PHONE, COMPLETED
    temp_data: Dict[str, Any] = {}

class ChatResponse(BaseModel):
    message: str
    next_state: str
    temp_data: Dict[str, Any]
    user_data: Optional[Dict[str, Any]] = None

@router.post("/process", response_model=ChatResponse)
def packet_process(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Process chat onboarding steps
    """
    state = request.state
    message = request.message.strip() if request.message else ""
    temp_data = request.temp_data
    
    # 1. NEW_USER: Initial Greeting
    if state == "NEW_USER":
        return ChatResponse(
            message="👋 Welcome to Udhaar.ai! Before we start, I need to register you.\n\nWhat is your full name?",
            next_state="ASK_NAME",
            temp_data={}
        )

    # 2. ASK_NAME: Validate and Ask Phone
    if state == "ASK_NAME":
        if len(message) < 2:
            return ChatResponse(
                message="Please enter a valid name (at least 2 characters).",
                next_state="ASK_NAME",
                temp_data=temp_data
            )
        
        temp_data["name"] = message
        return ChatResponse(
            message=f"Thanks {message}! Now please enter your 10-digit phone number.",
            next_state="ASK_PHONE",
            temp_data=temp_data
        )

    # 3. ASK_PHONE: Validate, Check DB, Register/Login
    if state == "ASK_PHONE":
        # Basic validation
        import re
        phone = re.sub(r'\D', '', message) # remove non-digits
        
        if len(phone) < 10:
             return ChatResponse(
                message="Please enter a valid 10-digit phone number.",
                next_state="ASK_PHONE",
                temp_data=temp_data
            )
        
        # Check if user exists
        existing = CustomerService.get_customer_by_phone(db, phone)
        
        if existing:
            # Login successful
            # Notify Vendor of Login (Optional, but good for visibility)
            try:
                from app.services.notification_service import NotificationService
                NotificationService.create_notification(
                    db, 
                    type="CUSTOMER_LOGIN", 
                    message=f"Customer Active: {existing.name} ({existing.phone})",
                    related_id=existing.id
                )
            except Exception:
                pass

            return ChatResponse(
                message=f"Welcome back, {existing.name}! ✅\nYou are now logged in.",
                next_state="COMPLETED",
                temp_data={},
                user_data={"id": existing.id, "name": existing.name, "phone": existing.phone}
            )
        
        # Register new user
        from app.schemas.customer import CustomerCreate
        try:
            new_customer = CustomerCreate(name=temp_data.get("name", "Guest"), phone=phone)
            customer = CustomerService.create_customer(db, new_customer)
            
            # Create Notification for Vendor
            try:
                from app.services.notification_service import NotificationService
                import threading
                # Use threading to not block response if notification fails/slows
                # For sqlite, we need to be careful with threads, so let's do synchronous but safe
                NotificationService.create_notification(
                    db, 
                    type="NEW_CUSTOMER", 
                    message=f"New Customer Added: {customer.name} ({customer.phone})",
                    related_id=customer.id
                )
            except Exception as ne:
                print(f"Notification error: {ne}")

            return ChatResponse(
                message="✅ Registration completed! You can now place orders.\n\nTry typing: 'Send 5 paracetamol'",
                next_state="COMPLETED",
                temp_data={},
                user_data={"id": customer.id, "name": customer.name, "phone": customer.phone}
            )
        except Exception as e:
            return ChatResponse(
                message=f"Error registering: {str(e)}. Please try again.",
                next_state="ASK_PHONE",
                temp_data=temp_data
            )

    return ChatResponse(message="Error: Unknown state", next_state="NEW_USER", temp_data={})
