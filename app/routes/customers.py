"""
Customer API routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.customer import CustomerCreate, CustomerResponse
from app.services.customer_service import CustomerService
from typing import List

router = APIRouter(prefix="/customers", tags=["customers"])


@router.post("/", response_model=CustomerResponse, status_code=201)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    """
    Create a new customer
    
    - **name**: Customer name (required)
    - **phone**: Customer phone number (required, unique)
    - **language_preference**: Preferred language code (default: 'en')
    """
    # Check if phone already exists
    existing = CustomerService.get_customer_by_phone(db, customer.phone)
    if existing:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    
    return CustomerService.create_customer(db, customer)


@router.get("/", response_model=List[CustomerResponse])
def get_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all customers with pagination
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100)
    """
    return CustomerService.get_all_customers(db, skip, limit)


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    """
    Get a specific customer by ID
    """
    customer = CustomerService.get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer
