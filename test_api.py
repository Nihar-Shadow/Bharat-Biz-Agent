"""
Test the OCR API directly to see what it returns
"""
import requests
import json

print("=" * 60)
print("TESTING OCR API ENDPOINT")
print("=" * 60)

# Test with a simple GET to check if server is running
try:
    response = requests.get("http://localhost:8000/health", timeout=5)
    print(f"✅ Backend server is running")
    print(f"   Health check: {response.status_code}")
except Exception as e:
    print(f"❌ Backend server not responding: {e}")
    exit(1)

# Now let's check what the OCR service module says
print("\n" + "=" * 60)
print("CHECKING OCR SERVICE MODULE")
print("=" * 60)

import sys
sys.path.insert(0, 'c:\\Nurothon')

from app.services.ocr_service import DEMO_MODE, TESSERACT_AVAILABLE

print(f"TESSERACT_AVAILABLE: {TESSERACT_AVAILABLE}")
print(f"DEMO_MODE: {DEMO_MODE}")

if DEMO_MODE:
    print("\n❌ PROBLEM: Backend is in DEMO MODE!")
    print("   The OCR service thinks Tesseract is not available")
else:
    print("\n✅ Backend has Real OCR enabled")

print("=" * 60)
