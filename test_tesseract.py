"""
Quick test to verify Tesseract OCR is working
"""
import os
import sys

print("🔍 Testing Tesseract OCR Installation...\n")

# Check if pytesseract is installed
try:
    import pytesseract
    print("✅ pytesseract library is installed")
except ImportError:
    print("❌ pytesseract library not found")
    print("   Run: pip install pytesseract")
    sys.exit(1)

# Check if Tesseract executable exists
tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
if os.path.exists(tesseract_path):
    print(f"✅ Tesseract executable found at: {tesseract_path}")
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
else:
    print(f"❌ Tesseract executable not found at: {tesseract_path}")
    sys.exit(1)

# Try to get version
try:
    version = pytesseract.get_tesseract_version()
    print(f"✅ Tesseract version: {version}")
    print("\n🎉 SUCCESS! Tesseract OCR is working!")
    print("\n📋 Next steps:")
    print("   1. Restart your backend server")
    print("   2. Go to: http://localhost:3000/bill-upload.html")
    print("   3. Upload a real bill image")
    print("   4. Enjoy real OCR! (No more demo mode)")
except Exception as e:
    print(f"❌ Error testing Tesseract: {e}")
    sys.exit(1)
