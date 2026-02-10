"""
Customer service - business logic for customer operations
"""
from sqlalchemy.orm import Session
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate
from typing import List, Optional


class CustomerService:
    """Service class for customer operations"""
    
    @staticmethod
    def create_customer(db: Session, customer_data: CustomerCreate) -> Customer:
        """Create a new customer"""
        customer = Customer(
            name=customer_data.name,
            phone=customer_data.phone,
            language_preference=customer_data.language_preference
        )
        db.add(customer)
        db.commit()
        db.refresh(customer)
        return customer
    
    @staticmethod
    def get_customer(db: Session, customer_id: int) -> Optional[Customer]:
        """Get customer by ID"""
        return db.query(Customer).filter(Customer.id == customer_id).first()
    
    @staticmethod
    def get_all_customers(db: Session, skip: int = 0, limit: int = 100) -> List[Customer]:
        """Get all customers with pagination"""
        return db.query(Customer).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_customer_by_phone(db: Session, phone: str) -> Optional[Customer]:
        """Get customer by phone number"""
        return db.query(Customer).filter(Customer.phone == phone).first()
