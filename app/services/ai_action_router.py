"""
AI Action Router - Routes intents to backend API calls

This module:
- Takes intent from AI Agent Engine
- Routes to appropriate backend service
- Logs all actions to AI log
- Returns structured response
"""
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.services.ai_agent_engine import AIAgentEngine, Intent
from app.services.customer_service import CustomerService
from app.services.product_service import ProductService
from app.services.order_service import OrderService
from app.services.invoice_service import InvoiceService
from app.services.ai_logger_service import AILoggerService
from app.schemas.customer import CustomerCreate
from app.schemas.product import ProductCreate
from app.schemas.order import OrderCreate, OrderItemCreate
from fastapi import HTTPException



# Simple in-memory context store (for hackathon/demo purposes)
# In production, use Redis or database with session IDs
AI_CONTEXT = {}

class AIActionRouter:
    """
    Routes AI-detected intents to backend actions
    """
    
    def __init__(self, db: Session):
        """
        Initialize router with database session
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db
        self.engine = AIAgentEngine()

    def _find_best_match(self, search_term: str, products: list) -> Optional[Any]:
        """
        Find the best matching product using a scoring system
        
        Args:
            search_term: The product name to search for
            products: List of Product objects
            
        Returns:
            Best matching Product object or None
        """
        search_term = search_term.lower().strip()
        best_product = None
        best_score = 0
        
        for p in products:
            p_name = p.name.lower()
            score = 0
            
            # Rule 1: Exact Match (100 pts)
            if p_name == search_term:
                score = 100
                
            # Rule 2: Contains Match (80 pts)
            elif search_term in p_name:
                # Deduct points for extra length to prefer "Keyboard" over "Logitech Keyboard" 
                # if search is just "Keyboard"
                score = 80 - (len(p_name) - len(search_term))
                
            # Rule 3: Word Intersection (10 pts per word)
            else:
                p_words = set(p_name.split())
                s_words = set(search_term.split())
                common_words = p_words.intersection(s_words)
                if common_words:
                    score = len(common_words) * 10
                    # Bonus if the first word matches (likely brand name)
                    if p_name.split()[0] == search_term.split()[0]:
                        score += 5
            
            if score > best_score:
                best_score = score
                best_product = p
                
        # Fallback: Fuzzy matching if score is low
        if best_score < 20:
             from difflib import get_close_matches
             p_names = [p.name.lower() for p in products]
             matches = get_close_matches(search_term, p_names, n=1, cutoff=0.6)
             if matches:
                 for p in products:
                     if p.name.lower() == matches[0]:
                         return p
                         
        return best_product
    
    def process_message(self, message: str) -> Dict[str, Any]:
        """
        Process natural language message and execute backend action
        
        Args:
            message: Natural language input
            
        Returns:
            Dictionary with intent, action result, and metadata
        """
        global AI_CONTEXT
        
        # Check if we are waiting for specific info
        if AI_CONTEXT.get("status") == "waiting_for_info":
            missing_field = AI_CONTEXT.get("missing_field")
            prev_intent_name = AI_CONTEXT.get("intent")
            prev_entities = AI_CONTEXT.get("entities", {})
            
            # If waiting for product name, treat message as product name
            if missing_field == "product_name":
                # Create synthetic intent with merged info
                prev_entities["product_name"] = message.strip()
                
                # Re-construct intent
                intent = Intent(
                    name=prev_intent_name,
                    confidence=1.0, # High confidence since we asked for it
                    entities=prev_entities
                )
                
                # Clear context
                AI_CONTEXT = {}
                
                # Skip detection and go straight to execution
                return self._execute_intent(intent, message)
        
        # Normal Intent Detection
        intent = self.engine.detect_intent(message)
        
        # Log the AI action
        AILoggerService.log_action(
            db=self.db,
            action_type=f"AI_INTENT_DETECTED_{intent.name.upper()}",
            input_text=message,
            output_action=f"Intent: {intent.name}, Confidence: {intent.confidence:.2f}"
        )
        
        return self._execute_intent(intent, message)

    def _execute_intent(self, intent: Intent, message: str) -> Dict[str, Any]:
        """Execute the identified intent"""
        global AI_CONTEXT
        
        # Clear context on new intent unless we set it again
        AI_CONTEXT = {}

        # Route to appropriate action
        try:
            if intent.name == "create_order":
                result = self._handle_create_order(intent, message)
            elif intent.name == "check_inventory":
                result = self._handle_check_inventory(intent, message)
            elif intent.name == "list_products":
                result = self._handle_list_products(intent, message)
            elif intent.name == "add_product":
                result = self._handle_add_product(intent, message)
            elif intent.name == "generate_invoice":
                result = self._handle_generate_invoice(intent, message)
            elif intent.name == "add_customer":
                result = self._handle_add_customer(intent, message)
            elif intent.name == "payment_reminder_suggestion":
                result = self._handle_payment_reminder(intent, message)
            else:
                result = {
                    "status": "unknown_intent",
                    "message": "I didn't understand that. Can you rephrase?",
                    "suggestions": [
                        "Create an order",
                        "Check inventory",
                        "Generate invoice",
                        "Add customer",
                        "Payment reminder"
                    ]
                }
        except Exception as e:
            result = {
                "status": "error",
                "message": str(e)
            }
            
            # Log error
            AILoggerService.log_action(
                db=self.db,
                action_type="AI_ACTION_ERROR",
                input_text=message,
                output_action=f"Error: {str(e)}"
            )
        
        # Result handling for missing info (Set Context)
        if result.get("status") == "missing_info":
            AI_CONTEXT = {
                "status": "waiting_for_info",
                "intent": intent.name,
                "entities": intent.entities,
                "missing_field": result.get("missing")[0] if result.get("missing") else None
            }
        
        # Return complete response
        return {
            "intent": intent.name,
            "confidence": intent.confidence,
            "entities": intent.entities,
            "action_result": result,
            "original_message": message
        }
    
    def _handle_create_order(self, intent: Intent, message: str) -> Dict[str, Any]:
        """Handle create_order intent"""
        entities = intent.entities
        
        # Validate required entities
        if "customer_name" not in entities:
            return {
                "status": "missing_info",
                "message": "Please provide customer name",
                "missing": ["customer_name"]
            }
        
        if "product_name" not in entities:
            return {
                "status": "missing_info",
                "message": "Please provide product name",
                "missing": ["product_name"]
            }
        
        # Find or suggest customer
        customer = None
        
        # 1. Try by phone if provided
        if "phone" in entities:
             customer = CustomerService.get_customer_by_phone(self.db, entities["phone"])
        
        # 2. Try by name (fuzzy) if no customer found yet
        if not customer:
            customers = CustomerService.get_all_customers(self.db)
            customer_names = [c.name.lower() for c in customers]
            from difflib import get_close_matches
            
            # Use 0.8 cutoff for customer names to avoid wrong person
            matches = get_close_matches(
                entities["customer_name"].lower(), 
                customer_names, 
                n=1, 
                cutoff=0.8
            )
            
            if matches:
                customer = next(c for c in customers if c.name.lower() == matches[0])
        
        # 3. Auto-create if still not found (The FIX)
        is_new_customer = False
        if not customer:
            import time
            import random
            
            # Generate ID for guest
            guest_id = f"{int(time.time())}{random.randint(100,999)}"
            phone = entities.get("phone", f"GUEST-{guest_id}")
            
            customer_data = CustomerCreate(
                name=entities["customer_name"],
                phone=phone,
                language_preference="en"
            )
            
            try:
                customer = CustomerService.create_customer(self.db, customer_data)
                is_new_customer = True
                
                # Log auto-creation
                AILoggerService.log_action(
                    db=self.db,
                    action_type="AI_AUTO_CREATED_CUSTOMER",
                    input_text=message,
                    output_action=f"Auto-created customer {customer.name} (Phone: {customer.phone})"
                )
            except Exception as e:
                 # Fallback if creation fails (e.g. duplicate phone unique constraint)
                 return {
                    "status": "error",
                    "message": f"Could not create customer: {str(e)}"
                 }
        
        # Find product
        products = ProductService.get_all_products(self.db)
        product = None
        product = self._find_best_match(entities["product_name"], products)
        
        if not product:
            available = [p.name for p in products[:10]]
            return {
                "status": "product_not_found",
                "message": f"Product '{entities['product_name']}' not found",
                "available_products": available
            }
        
        # Get quantity (default to 1)
        quantity = entities.get("quantity", 1)
        
        # Check stock
        if product.stock_quantity < quantity:
            return {
                "status": "insufficient_stock",
                "message": f"Only {product.stock_quantity} {product.name} available",
                "available": product.stock_quantity,
                "requested": quantity
            }
        
        # Create order
        order_data = OrderCreate(
            customer_id=customer.id,
            items=[
                OrderItemCreate(
                    product_id=product.id,
                    quantity=quantity
                )
            ]
        )
        
        order = OrderService.create_order(self.db, order_data)
        
        # Auto-generate Invoice
        invoice = InvoiceService.generate_invoice(self.db, order.id)
        
        # Log success
        AILoggerService.log_action(
            db=self.db,
            action_type="AI_ORDER_CREATED",
            input_text=message,
            output_action=f"Order #{order.id} created & Invoice generated for {customer.name}, Total: ₹{order.order_total:.2f}"
        )
        
        msg_suffix = " (New Customer Auto-Created)" if is_new_customer else ""
        return {
            "status": "success",
            "message": f"Order created and invoice generated! Order ID: {order.id}{msg_suffix}",
            "order_id": order.id,
            "invoice_id": invoice.id,
            "customer": customer.name,
            "product": product.name,
            "quantity": quantity,
            "total": order.order_total,
            "download_url": f"/api/v1/invoices/{invoice.id}/download"
        }
    
    def _handle_list_products(self, intent: Intent, message: str) -> Dict[str, Any]:
        """Handle list_products intent - show all products with stock"""
        try:
            products = ProductService.get_all_products(self.db, limit=100)
            
            if not products:
                return {
                    "status": "error",
                    "message": "No products found in inventory"
                }
            
            # Format product list
            product_list = []
            for p in products:
                product_list.append({
                    "name": p.name,
                    "stock": p.stock_quantity,
                    "price": float(p.price),
                    "needs_reorder": p.needs_reorder
                })
            
            return {
                "status": "success",
                "message": f"Found {len(products)} products",
                "products": product_list,
                "total_count": len(products)
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error fetching products: {str(e)}"
            }
    
    def _handle_check_inventory(self, intent: Intent, message: str) -> Dict[str, Any]:
        """Handle check_inventory intent"""
        entities = intent.entities
        
        if "product_name" in entities:
            # Check specific product
            products = ProductService.get_all_products(self.db)
            product = None
            product = self._find_best_match(entities["product_name"], products)
            
            if not product:
                # Show available products as suggestions
                available = [p.name for p in products[:10]]
                return {
                    "status": "product_not_found",
                    "message": f"Product '{entities['product_name']}' not found",
                    "available_products": available,
                    "suggestion": "Try one of the available products"
                }
            
            # Log action
            AILoggerService.log_action(
                db=self.db,
                action_type="AI_INVENTORY_CHECKED",
                input_text=message,
                output_action=f"Stock for {product.name}: {product.stock_quantity} units"
            )
            
            return {
                "status": "success",
                "product": product.name,
                "stock": product.stock_quantity,
                "price": product.price,
                "needs_reorder": product.needs_reorder,
                "message": f"{product.name}: {product.stock_quantity} units available at ₹{product.price}"
            }
        else:
            # Show all low stock products
            low_stock = ProductService.get_low_stock_products(self.db)
            
            return {
                "status": "success",
                "message": f"Found {len(low_stock)} products with low stock",
                "low_stock_products": [
                    {
                        "name": p.name,
                        "stock": p.stock_quantity,
                        "threshold": p.reorder_threshold
                    }
                    for p in low_stock
                ]
            }
    
    def _handle_generate_invoice(self, intent: Intent, message: str) -> Dict[str, Any]:
        """Handle generate_invoice intent"""
        entities = intent.entities
        
        if "order_id" not in entities:
            return {
                "status": "missing_info",
                "message": "Please provide order ID",
                "missing": ["order_id"]
            }
        
        order_id = entities["order_id"]
        
        # Check if order exists
        order = OrderService.get_order(self.db, order_id)
        if not order:
            return {
                "status": "order_not_found",
                "message": f"Order #{order_id} not found"
            }
        
        # Generate invoice
        invoice = InvoiceService.generate_invoice(self.db, order_id)
        
        # Log action
        AILoggerService.log_action(
            db=self.db,
            action_type="AI_INVOICE_GENERATED",
            input_text=message,
            output_action=f"Invoice #{invoice.id} generated for Order #{order_id}"
        )
        
        return {
            "status": "success",
            "message": f"Invoice generated successfully!",
            "invoice_id": invoice.id,
            "order_id": order_id,
            "file_path": invoice.file_path,
            "download_url": f"/api/v1/invoices/{invoice.id}/download"
        }
    
    def _handle_add_customer(self, intent: Intent, message: str) -> Dict[str, Any]:
        """Handle add_customer intent"""
        entities = intent.entities
        
        if "customer_name" not in entities:
            return {
                "status": "missing_info",
                "message": "Please provide customer name",
                "missing": ["customer_name"]
            }
        
        if "phone" not in entities:
            return {
                "status": "missing_info",
                "message": "Please provide phone number",
                "missing": ["phone"]
            }
        
        # Check if customer already exists
        existing = CustomerService.get_customer_by_phone(self.db, entities["phone"])
        if existing:
            return {
                "status": "already_exists",
                "message": f"Customer with phone {entities['phone']} already exists",
                "customer_id": existing.id,
                "customer_name": existing.name
            }
        
        # Create customer
        customer_data = CustomerCreate(
            name=entities["customer_name"],
            phone=entities["phone"],
            language_preference="en"  # Default, can be enhanced
        )
        
        customer = CustomerService.create_customer(self.db, customer_data)
        
        # Log action
        AILoggerService.log_action(
            db=self.db,
            action_type="AI_CUSTOMER_ADDED",
            input_text=message,
            output_action=f"Customer {customer.name} added with ID {customer.id}"
        )
        
        return {
            "status": "success",
            "message": f"Customer '{customer.name}' added successfully!",
            "customer_id": customer.id,
            "customer_name": customer.name,
            "phone": customer.phone
        }
    
    def _handle_add_product(self, intent: Intent, message: str) -> Dict[str, Any]:
        """Handle add_product intent - vendor adds new product"""
        entities = intent.entities
        
        # Required: product name, price, stock quantity
        # Optional: reorder threshold (default 10)
        
        if "product_name" not in entities:
            return {
                "status": "missing_info",
                "message": "Please provide product name",
                "missing": ["product_name"],
                "example": "Add product Laptop price 50000 stock 10"
            }
        
        if "price" not in entities:
            return {
                "status": "missing_info",
                "message": f"Please provide price for {entities['product_name']}",
                "missing": ["price"],
                "example": f"Add {entities['product_name']} price 5000 stock 20"
            }
        
        if "quantity" not in entities:
            return {
                "status": "missing_info",
                "message": f"Please provide stock quantity for {entities['product_name']}",
                "missing": ["quantity"],
                "example": f"Add {entities['product_name']} price {entities['price']} stock 15"
            }
        
        # Check if product already exists
        products = ProductService.get_all_products(self.db)
        
        # Use find_best_match but verify it's a strong match
        existing_product = self._find_best_match(entities["product_name"], products)
        
        # Only consider it a match for update if names are very similar
        is_match = False
        if existing_product:
             s_term = entities["product_name"].lower().strip()
             p_term = existing_product.name.lower().strip()
             # Allow exact match or if one contains the other
             if s_term == p_term or s_term in p_term or p_term in s_term:
                 is_match = True

        if is_match:
            # Update existing product
            quantity = int(entities["quantity"])
            price = float(entities["price"])
            
            existing_product.stock_quantity += quantity
            existing_product.price = price # Update price to latest
            if "reorder_threshold" in entities:
                existing_product.reorder_threshold = entities["reorder_threshold"]
            
            self.db.commit()
            self.db.refresh(existing_product)
            
            product = existing_product
            action_type = "AI_PRODUCT_UPDATED"
            success_msg = f"Updated stock for '{product.name}'!"
            
        else:
            # Create new product
            reorder_threshold = entities.get("reorder_threshold", 10)  # Default threshold
            
            product_data = ProductCreate(
                name=entities["product_name"],
                price=float(entities["price"]),
                stock_quantity=int(entities["quantity"]),
                reorder_threshold=reorder_threshold
            )
            
            product = ProductService.create_product(self.db, product_data)
            action_type = "AI_PRODUCT_ADDED"
            success_msg = f"Product '{product.name}' added successfully!"
        
        # Log action
        AILoggerService.log_action(
            db=self.db,
            action_type=action_type,
            input_text=message,
            output_action=f"{success_msg} (ID: {product.id})"
        )
        
        return {
            "status": "success",
            "message": success_msg,
            "product_id": product.id,
            "product_name": product.name,
            "price": float(product.price),
            "stock": product.stock_quantity,
            "reorder_threshold": product.reorder_threshold
        }
    
    def _handle_payment_reminder(self, intent: Intent, message: str) -> Dict[str, Any]:
        """Handle payment_reminder_suggestion intent"""
        entities = intent.entities
        
        # This is a suggestion feature - doesn't execute action
        # In production, this would integrate with SMS/WhatsApp API
        
        customer_name = entities.get("customer_name", "customer")
        
        # Log action
        AILoggerService.log_action(
            db=self.db,
            action_type="AI_PAYMENT_REMINDER_SUGGESTED",
            input_text=message,
            output_action=f"Payment reminder suggested for {customer_name}"
        )
        
        return {
            "status": "suggestion",
            "message": f"Payment reminder suggestion for {customer_name}",
            "suggested_message": f"Dear {customer_name}, this is a friendly reminder about your pending payment. Please clear your dues at your earliest convenience. Thank you!",
            "channels": ["SMS", "WhatsApp", "Email"],
            "note": "This is a suggestion. Actual sending requires integration with messaging services."
        }


# Example usage
if __name__ == "__main__":
    from app.database import SessionLocal
    
    db = SessionLocal()
    router = AIActionRouter(db)
    
    # Test messages
    test_messages = [
        "Order 2 laptops for Rahul phone 9876543210",
        "Check stock of mouse",
        "Generate invoice for order 1",
        "Add customer Priya 9123456789"
    ]
    
    for msg in test_messages:
        print(f"\nInput: {msg}")
        result = router.process_message(msg)
        print(f"Result: {result}")
    
    db.close()
