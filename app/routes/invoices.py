"""
Invoice API routes
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.invoice import InvoiceResponse
from app.services.invoice_service import InvoiceService
import os

router = APIRouter(prefix="/invoices", tags=["invoices"])


@router.post("/generate/{order_id}", response_model=InvoiceResponse, status_code=201)
def generate_invoice(order_id: int, db: Session = Depends(get_db)):
    """
    Generate a PDF invoice for an order
    
    - **order_id**: Order ID (required)
    
    If an invoice already exists for this order, returns the existing invoice.
    Otherwise, generates a new PDF invoice with:
    - Order details
    - Customer information
    - Itemized list of products
    - Total amount
    """
    return InvoiceService.generate_invoice(db, order_id)


@router.get("/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    """
    Get invoice details by ID
    """
    invoice = InvoiceService.get_invoice(db, invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice


@router.get("/{invoice_id}/download")
def download_invoice(invoice_id: int, db: Session = Depends(get_db)):
    """
    Download the PDF invoice file
    """
    invoice = InvoiceService.get_invoice(db, invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    if not os.path.exists(invoice.file_path):
        raise HTTPException(status_code=404, detail="Invoice file not found")
    
    return FileResponse(
        path=invoice.file_path,
        media_type="application/pdf",
        filename=f"invoice_{invoice_id}.pdf"
    )


@router.get("/order/{order_id}", response_model=InvoiceResponse)
def get_invoice_by_order(order_id: int, db: Session = Depends(get_db)):
    """
    Get invoice by order ID
    """
    invoice = InvoiceService.get_invoice_by_order(db, order_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found for this order")
    return invoice
