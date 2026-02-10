"""
Invoice service - business logic for invoice generation
"""
from sqlalchemy.orm import Session
from app.models.invoice import Invoice
from app.models.order import Order
from app.services.ai_logger_service import AILoggerService
from app.config import settings
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch
from typing import Optional
from fastapi import HTTPException
from datetime import datetime


class InvoiceService:
    """Service class for invoice operations"""
    
    @staticmethod
    def generate_invoice(db: Session, order_id: int) -> Invoice:
        """Generate PDF invoice for an order"""
        # Check if invoice already exists
        existing_invoice = db.query(Invoice).filter(Invoice.order_id == order_id).first()
        if existing_invoice:
            return existing_invoice
        
        # Get order with items
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        # Generate PDF
        filename = f"invoice_{order_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        file_path = settings.INVOICE_DIR / filename
        
        InvoiceService._create_pdf(order, str(file_path))
        
        # Save invoice record
        invoice = Invoice(
            order_id=order_id,
            file_path=str(file_path)
        )
        db.add(invoice)
        db.commit()
        db.refresh(invoice)
        
        # Log AI action
        AILoggerService.log_action(
            db=db,
            action_type="INVOICE_GENERATED",
            input_text=f"Generate invoice for order {order_id}",
            output_action=f"Invoice {invoice.id} created at {file_path}"
        )
        
        return invoice
    
    @staticmethod
    def _create_pdf(order: Order, file_path: str):
        """Create PDF invoice using ReportLab"""
        doc = SimpleDocTemplate(file_path, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title = Paragraph(f"<b>INVOICE #{order.id}</b>", styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 0.3 * inch))
        
        # Order info
        info_text = f"""
        <b>Date:</b> {order.created_at.strftime('%Y-%m-%d %H:%M')}<br/>
        <b>Customer ID:</b> {order.customer_id}<br/>
        <b>Customer Name:</b> {order.customer.name}<br/>
        <b>Phone:</b> {order.customer.phone}
        """
        info = Paragraph(info_text, styles['Normal'])
        elements.append(info)
        elements.append(Spacer(1, 0.3 * inch))
        
        # Items table
        data = [['Product', 'Quantity', 'Price', 'Subtotal']]
        for item in order.items:
            data.append([
                item.product.name,
                str(item.quantity),
                f"${item.price:.2f}",
                f"${item.subtotal:.2f}"
            ])
        
        # Add total
        data.append(['', '', '<b>TOTAL</b>', f'<b>${order.order_total:.2f}</b>'])
        
        table = Table(data, colWidths=[3*inch, 1*inch, 1*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, -1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.5 * inch))
        
        # Footer
        footer = Paragraph("<i>Thank you for your business!</i>", styles['Normal'])
        elements.append(footer)
        
        doc.build(elements)
    
    @staticmethod
    def get_invoice(db: Session, invoice_id: int) -> Optional[Invoice]:
        """Get invoice by ID"""
        return db.query(Invoice).filter(Invoice.id == invoice_id).first()
    
    @staticmethod
    def get_invoice_by_order(db: Session, order_id: int) -> Optional[Invoice]:
        """Get invoice by order ID"""
        return db.query(Invoice).filter(Invoice.order_id == order_id).first()
