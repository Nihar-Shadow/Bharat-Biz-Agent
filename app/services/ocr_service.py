"""
OCR Service for Bill Processing
Extracts product information from bill images
"""
import re
import os
from typing import List, Dict, Optional
from PIL import Image
import io

# Try to import pytesseract
try:
    import pytesseract
    TESSERACT_AVAILABLE = True
    
    # For Windows, set tesseract path directly
    if os.name == 'nt':  # Windows
        # Try direct path first
        direct_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        if os.path.exists(direct_path):
            pytesseract.pytesseract.tesseract_cmd = direct_path
            print(f"✅ Tesseract found at: {direct_path}")
        else:
            # Try other common paths
            possible_paths = [
                r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
                r'C:\Tesseract-OCR\tesseract.exe',
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    pytesseract.pytesseract.tesseract_cmd = path
                    print(f"✅ Tesseract found at: {path}")
                    break
except ImportError:
    TESSERACT_AVAILABLE = False
    pytesseract = None


# Test if Tesseract actually works
DEMO_MODE = True  # Default to demo mode
TESSERACT_CMD_PATH = None

if TESSERACT_AVAILABLE and pytesseract:
    # Check if we found a valid path
    tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    if os.path.exists(tesseract_path):
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
        TESSERACT_CMD_PATH = tesseract_path
        DEMO_MODE = False  # Tesseract executable exists, disable demo mode
        print(f"✅ Tesseract OCR is active at: {tesseract_path}")
        print("🎉 Real OCR processing enabled!")
    else:
        print(f"⚠️ Tesseract executable not found at: {tesseract_path}")
        print("📝 Using DEMO MODE")
else:
    print("⚠️ pytesseract library not available")
    print("📝 Using DEMO MODE - Install Tesseract for real OCR")


class BillItem:
    """Represents a single item from a bill"""
    def __init__(self, product_name: str, quantity: int, price: float):
        self.product_name = product_name
        self.quantity = quantity
        self.price = price
    
    def to_dict(self):
        return {
            "product_name": self.product_name,
            "quantity": self.quantity,
            "price": self.price
        }


class OCRBillProcessor:
    """Process bill images and extract structured data"""
    
    def __init__(self):
        # Common patterns for bill items
        self.price_pattern = re.compile(r'₹?\s*(\d+(?:,\d{3})*(?:\.\d{2})?)')
        self.quantity_pattern = re.compile(r'(\d+)\s*(?:x|X|pcs?|pieces?|units?)?')
        
    def extract_text_from_image(self, image_bytes: bytes) -> str:
        """Extract text from image using OCR"""
        if DEMO_MODE:
            # Return demo text when Tesseract is not available
            return """DEMO RESTAURANT BILL
            ==================
            Burger        2x  ₹150.00
            Pizza         1x  ₹450.00
            French Fries  3x  ₹80.00
            Coke          2x  ₹50.00
            ==================
            Total:        ₹940.00
            
            NOTE: This is DEMO data. Install Tesseract OCR for real bill processing.
            """
        
        try:
            if not TESSERACT_AVAILABLE:
                raise Exception("Tesseract is not installed. Please install Tesseract OCR.")
            
            image = Image.open(io.BytesIO(image_bytes))
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Perform OCR
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            raise Exception(f"OCR failed: {str(e)}")
    
    def parse_bill_text(self, text: str) -> List[BillItem]:
        """Parse extracted text to find products, quantities, and prices"""
        items = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or len(line) < 5:
                continue
            
            # Try to extract item information
            item = self._parse_line(line)
            if item:
                items.append(item)
        
        return items
    
    def _parse_line(self, line: str) -> Optional[BillItem]:
        """Parse a single line to extract product, quantity, and price"""
        # Skip common header/footer lines and non-product lines
        skip_keywords = ['total', 'subtotal', 'tax', 'gst', 'cgst', 'sgst', 'discount', 
                        'thank you', 'invoice', 'bill', 'receipt', 'date', 'time', 'note', 'demo',
                        'card', 'payment', 'cash', 'change', 'phone', 'address', 'store']
        if any(keyword in line.lower() for keyword in skip_keywords):
            return None
        
        # Skip lines that look like phone numbers or dates
        if re.search(r'\(\d{3}\)\s*\d{3}-\d{4}', line):  # Phone number pattern
            return None
        if re.search(r'\d{2}/\d{2}/\d{4}', line):  # Date pattern
            return None
        
        # Find all price-like numbers (with $ or ₹ or decimal)
        prices = self.price_pattern.findall(line)
        
        if not prices:
            return None
        
        # Get the last number as price (most likely the item price)
        price_str = prices[-1].replace(',', '')
        try:
            price = float(price_str)
        except ValueError:
            return None
        
        # Skip if price is unreasonably high (likely not a product price)
        if price > 10000:
            return None
        
        # Look for explicit quantity patterns like "2x", "3 x", "Qty: 2"
        qty_match = re.search(r'(?:qty|quantity|x)\s*[:=]?\s*(\d+)|(\d+)\s*x\s', line, re.IGNORECASE)
        quantity = 1  # Default quantity
        
        if qty_match:
            quantity = int(qty_match.group(1) or qty_match.group(2))
        else:
            # Check if there's a number followed by "CT" (count) in the product name
            # But don't use it as quantity, it's part of the product description
            pass
        
        # Extract product name
        # Remove price from the line
        product_line = line
        for p in prices:
            product_line = product_line.replace(p, '')
        
        # Remove currency symbols and clean up
        product_line = re.sub(r'[₹$]', '', product_line)
        product_line = re.sub(r'\s+', ' ', product_line).strip()
        
        # Remove quantity indicators if found
        if qty_match:
            product_line = re.sub(r'(?:qty|quantity|x)\s*[:=]?\s*\d+|\d+\s*x\s', '', product_line, flags=re.IGNORECASE)
        
        product_name = product_line.strip()
        
        # Skip if product name is too short or empty
        if not product_name or len(product_name) < 2:
            return None
        
        # Skip if product name is just numbers
        if product_name.replace(' ', '').isdigit():
            return None
        
        return BillItem(product_name, quantity, price)
    
    def process_bill_image(self, image_bytes: bytes) -> Dict:
        """Main method to process bill image and return structured data"""
        try:
            # Extract text
            text = self.extract_text_from_image(image_bytes)
            
            # Parse items
            items = self.parse_bill_text(text)
            
            # Calculate total
            total_amount = sum(item.price * item.quantity for item in items)
            
            demo_warning = " (DEMO MODE - Install Tesseract for real OCR)" if DEMO_MODE else ""
            
            return {
                "success": True,
                "demo_mode": DEMO_MODE,
                "extracted_text": text,
                "items": [item.to_dict() for item in items],
                "total_items": len(items),
                "total_amount": total_amount,
                "message": f"Successfully extracted {len(items)} items from bill{demo_warning}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to process bill image",
                "install_instructions": "Install Tesseract OCR: https://github.com/UB-Mannheim/tesseract/wiki or run 'choco install tesseract'"
            }


# Singleton instance
ocr_processor = OCRBillProcessor()
