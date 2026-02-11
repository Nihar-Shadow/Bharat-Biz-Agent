"""
AI Agent Engine - Natural Language to Backend Action Converter

This module handles:
- Intent detection from natural language
- Entity extraction (customer, product, quantity, price)
- Hinglish support
- Spelling error tolerance
- Action routing to backend APIs
"""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import re
from difflib import get_close_matches
from sqlalchemy.orm import Session


@dataclass
class Intent:
    """Intent classification result"""
    name: str
    confidence: float
    entities: Dict[str, Any]


class AIAgentEngine:
    """
    AI Agent Engine for converting natural language to backend actions
    Supports English, Hindi, and Hinglish
    """
    
    # Intent patterns with keywords (English and Hinglish)
    INTENT_PATTERNS = {
        "create_order": [
            "order", "place order", "book", "buy", "purchase", "chahiye", 
            "lena hai", "order karo", "order dedo", "dedo", "bhejo",
            "send", "deliver", "ship", "dispatch", "bhej do"
        ],
        "check_inventory": [
            "stock", "inventory", "available", "kitna hai", "check stock",
            "stock check", "available hai", "kitne hai", "bacha hai"
        ],
        "list_products": [
            "list", "products", "all products", "show products", "product list",
            "sab products", "kitna baki", "baki hai", "list of products",
            "product kitna", "sabhi products", "dikhao products"
        ],
        "add_product": [
            "add product", "new product", "create product", "product add",
            "naaya product", "product banao", "add karo product", "product dalo",
            "insert product", "register product"
        ],
        "generate_invoice": [
            "invoice", "bill", "receipt", "bill banao", "invoice chahiye",
            "bill dedo", "receipt chahiye", "bill generate"
        ],
        "add_customer": [
            "add customer", "new customer", "register", "customer add",
            "naaya customer", "customer banao", "register karo"
        ],
        "payment_reminder_suggestion": [
            "payment", "reminder", "due", "pending", "payment reminder",
            "yaad dilao", "payment pending", "baaki hai", "baki payment"
        ]
    }
    
    # Common product names (for fuzzy matching)
    COMMON_PRODUCTS = [
        "laptop", "mouse", "keyboard", "cable", "charger", "headphone",
        "phone", "tablet", "monitor", "printer", "speaker", "paracetamol", "medicine"
    ]
    
    # Hinglish number words
    NUMBER_WORDS = {
        "ek": 1, "do": 2, "teen": 3, "char": 4, "paanch": 5,
        "chhe": 6, "saat": 7, "aath": 8, "nau": 9, "das": 10,
        "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10
    }
    
    def __init__(self):
        """Initialize AI Agent Engine"""
        self.intent_cache = {}
    
    def detect_intent(self, text: str) -> Intent:
        """
        Detect intent from natural language text
        
        Args:
            text: Natural language input (English/Hindi/Hinglish)
            
        Returns:
            Intent object with name, confidence, and entities
        """
        # Normalize text
        text_lower = text.lower().strip()
        
        # Check cache
        if text_lower in self.intent_cache:
            return self.intent_cache[text_lower]
        
        # Score each intent with improved logic
        intent_scores = {}
        for intent_name, keywords in self.INTENT_PATTERNS.items():
            score = 0
            for keyword in keywords:
                if keyword in text_lower:
                    # Multi-word phrases get much higher score
                    word_count = len(keyword.split())
                    if word_count > 1:
                        score += 5  # Strong match for phrases
                    else:
                        score += 2  # Regular match for single words
                elif self._fuzzy_match(keyword, text_lower):
                    # Fuzzy match gets lower score
                    score += 1
            intent_scores[intent_name] = score
        
        # Special rule for add_product: If "add" or "new" (or Hinglish variants) is present with "price" or "stock", 
        # and it's not a customer/order action, strongly favor add_product
        if any(k in text_lower for k in ["add", "new", "create", "naaya", "nava", "banao", "dalo"]) and \
           any(k in text_lower for k in ["price", "stock", "cost", "rate", "daam", "bharti"]) and \
           not any(k in text_lower for k in ["customer", "order", "bill", "invoice"]):
            intent_scores["add_product"] = intent_scores.get("add_product", 0) + 10
        
        # Get best intent
        if not intent_scores or max(intent_scores.values()) == 0:
            best_intent = "unknown"
            confidence = 0.0
        else:
            best_intent = max(intent_scores, key=intent_scores.get)
            max_score = intent_scores[best_intent]
            confidence = min(max_score / 5.0, 1.0)  # Normalize to 0-1
        
        # Extract entities
        entities = self.extract_entities(text_lower, best_intent)
        
        # Create intent object
        intent = Intent(
            name=best_intent,
            confidence=confidence,
            entities=entities
        )
        
        # Cache result
        self.intent_cache[text_lower] = intent
        
        return intent
    
    def extract_entities(self, text: str, intent: str) -> Dict[str, Any]:
        """
        Extract entities from text based on intent
        
        Args:
            text: Normalized text
            intent: Detected intent
            
        Returns:
            Dictionary of extracted entities
        """
        entities = {}
        
        # Extract customer name
        customer_name = self._extract_customer_name(text)
        if customer_name:
            entities["customer_name"] = customer_name
        
        # Extract product name
        product_name = self._extract_product_name(text)
        if product_name:
            entities["product_name"] = product_name
        
        # Extract quantity
        quantity = self._extract_quantity(text)
        if quantity:
            entities["quantity"] = quantity
        
        # Extract price
        price = self._extract_price(text)
        if price:
            entities["price"] = price
        
        # Extract phone number
        phone = self._extract_phone(text)
        if phone:
            entities["phone"] = phone
        
        # Extract order ID
        order_id = self._extract_order_id(text)
        if order_id:
            entities["order_id"] = order_id
        
        return entities
    
    def _extract_customer_name(self, text: str) -> Optional[str]:
        """Extract customer name from text"""
        # Patterns: "for <name>", "customer <name>", "naam <name>"
        patterns = [
            r"for\s+([A-Za-z]+(?:\s+[A-Za-z]+)?)",
            r"to\s+([A-Za-z]+(?:\s+[A-Za-z]+)?)",
            r"customer\s+([A-Za-z]+(?:\s+[A-Za-z]+)?)",
            r"naam\s+([A-Za-z]+(?:\s+[A-Za-z]+)?)",
            r"name\s+([A-Za-z]+(?:\s+[A-Za-z]+)?)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).title()
        
        return None

    def _extract_product_name(self, text: str) -> Optional[str]:
        """Extract product name from text with fuzzy matching"""
        text_lower = text.lower()

        # 1. Specialized extraction for "Add Product" intent
        # Look for pattern: "product <name> price" or "product <name> stock"
        # This allows multi-word names like "Logitech Keyboard"
        add_patterns = [
            r'product\s+(.*?)\s+(?:price|stock|cost|rate)',
            r'add\s+(?:new\s+)?(.*?)\s+(?:price|stock|cost|rate)',
            r'create\s+(?:new\s+)?(.*?)\s+(?:price|stock|cost|rate)',
        ]
        
        for pattern in add_patterns:
            match = re.search(pattern, text_lower)
            if match:
                candidate = match.group(1).strip()
                # Filter out obvious non-names
                if len(candidate) > 2 and not re.search(r'\d', candidate):
                    return candidate.title()

        # 2. Check for hyphenated part numbers or product codes (e.g., USB-HUB, LAP-001)
        part_pattern = r'\b([A-Za-z]+-[A-Za-z0-9]+)\b'
        match = re.search(part_pattern, text)
        if match:
            return match.group(1)

        # 3. Smart Fallback: Strip intent keywords, numbers, and price/stock patterns
        # This handles generic "Send 5 X" where X is unknown
        cleaned_text = text_lower
        
        # Remove specific "price 2000" or "stock 25" patterns first to avoid stripping numbers later incorrectly
        cleaned_text = re.sub(r'\b(price|stock|cost|rate|qty|quantity)\s*[:]?\s*\d+(?:\.\d+)?', '', cleaned_text)
        
        # Remove intent keywords
        for keywords in self.INTENT_PATTERNS.values():
            for k in keywords:
                # Use word boundary to avoid partial replacements
                cleaned_text = re.sub(r'\b' + re.escape(k) + r'\b', '', cleaned_text)
                
        # Remove remaining numbers and quantity units
        cleaned_text = re.sub(r'\b\d+\b', '', cleaned_text)
        cleaned_text = re.sub(r'\b(pieces|piece|units|unit|qty|quantity|nos|karo)\b', '', cleaned_text)
        
        # Remove stopwords
        cleaned_text = re.sub(r'\b(for|to|of|in|at|with)\b', '', cleaned_text)
        
        # Remove extra whitespace and special chars
        cleaned_text = re.sub(r'[^\w\s-]', '', cleaned_text)
        cleaned_text = " ".join(cleaned_text.split())
        
        if cleaned_text and len(cleaned_text) > 2:
            return cleaned_text.title()

        return None
    
    def _extract_quantity(self, text: str) -> Optional[int]:
        """Extract quantity from text"""
        
        # 1. Look for explicit stock/quantity keywords (high priority)
        # e.g. "stock 25", "qty 10", "10 units"
        explicit_patterns = [
            r'(?:stock|qty|quantity|units|pieces|pcs|count)\s*[:]?\s*(\d+)',
            r'(\d+)\s*(?:pieces|units|pcs|qty|quantity|stock)',
        ]
        
        for p in explicit_patterns:
            match = re.search(p, text, re.IGNORECASE)
            if match:
                return int(match.group(1))
        
        # 2. Fallback: Look for generic number, but careful to avoid price
        # Find all numbers
        all_numbers = re.finditer(r'\b(\d+)\b', text)
        
        for m in all_numbers:
            num = m.group(1)
            start_idx = m.start()
            
            # Context check: Is this number preceded by "price", "rs", "cost"?
            # Look at preceding 15 chars
            preceding = text[max(0, start_idx-15):start_idx].lower()
            if any(x in preceding for x in ['price', 'rs', 'cost', 'rate', '₹']):
                continue # Skip this number, it's a price
                
            # If we are here, it's likely a quantity (or ID, phone)
            # Typically quantity is small (< 1000) for retail, price is large
            # But "stock 2000" is possible.
            # If user just said "Send 2000", assumption is quantity.
            return int(num)

        # 3. Look for number words
        for word, num in self.NUMBER_WORDS.items():
            if word in text.lower():
                return num
        
        return None
    
    def _extract_price(self, text: str) -> Optional[float]:
        """Extract price from text"""
        # Patterns: "price 2000", "Rs 100", "₹100", "100 rupees", "100 rs"
        patterns = [
            r'price[:\s]+(\d+(?:\.\d{2})?)',  # "price 2000" or "price: 2000"
            r'(?:rs\.?|₹)\s*(\d+(?:\.\d{2})?)',  # "Rs 100" or "₹100"
            r'(\d+(?:\.\d{2})?)\s*(?:rupees|rs|inr)',  # "100 rupees"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return float(match.group(1))
        
        return None
    
    def _extract_phone(self, text: str) -> Optional[str]:
        """Extract phone number from text"""
        # Indian phone patterns
        patterns = [
            r'\+91[\s-]?\d{10}',
            r'\d{10}',
            r'\d{5}[\s-]\d{5}'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                phone = match.group(0)
                # Clean up
                phone = re.sub(r'[\s-]', '', phone)
                if not phone.startswith('+'):
                    phone = '+91' + phone if len(phone) == 10 else '+' + phone
                return phone
        
        return None
    
    def _extract_order_id(self, text: str) -> Optional[int]:
        """Extract order ID from text"""
        # Patterns: "order #123", "order 123", "order id 123"
        patterns = [
            r'order\s*#?\s*(\d+)',
            r'order\s+id\s+(\d+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return int(match.group(1))
        
        return None
    
    def _fuzzy_match(self, keyword: str, text: str, threshold: float = 0.8) -> bool:
        """Check if keyword fuzzy matches any word in text"""
        words = text.split()
        matches = get_close_matches(keyword, words, n=1, cutoff=threshold)
        return len(matches) > 0
    
    def to_json(self, intent: Intent) -> Dict[str, Any]:
        """
        Convert Intent to JSON format
        
        Args:
            intent: Intent object
            
        Returns:
            JSON-serializable dictionary
        """
        return {
            "intent": intent.name,
            "entities": intent.entities,
            "confidence": round(intent.confidence, 2)
        }


# Example usage
if __name__ == "__main__":
    engine = AIAgentEngine()
    
    # Test cases
    test_messages = [
        "Laptop chahiye 2 pieces for Rahul",
        "Check stock of mouse",
        "Generate bill for order 123",
        "Add new customer Priya phone 9876543210",
        "Payment reminder for Amit",
        "Order karo 5 cables Rs 500",
        "Kitne laptop available hai?",
        "Invoice dedo order #5 ka"
    ]
    
    print("AI Agent Engine - Test Results\n")
    for msg in test_messages:
        intent = engine.detect_intent(msg)
        result = engine.to_json(intent)
        print(f"Input: {msg}")
        print(f"Output: {result}\n")
