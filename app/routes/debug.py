"""
Add a debug endpoint to check OCR status
"""
from fastapi import APIRouter
from app.services.ocr_service import DEMO_MODE, TESSERACT_AVAILABLE, pytesseract
import os

router = APIRouter(prefix="/debug", tags=["debug"])


@router.get("/ocr-status")
async def get_ocr_status():
    """Check OCR configuration status"""
    
    status = {
        "tesseract_available": TESSERACT_AVAILABLE,
        "demo_mode": DEMO_MODE,
        "pytesseract_module": pytesseract is not None,
    }
    
    if pytesseract:
        try:
            status["tesseract_cmd"] = str(pytesseract.pytesseract.tesseract_cmd)
            status["tesseract_version"] = str(pytesseract.get_tesseract_version())
        except Exception as e:
            status["error"] = str(e)
    
    # Check if file exists
    tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    status["tesseract_file_exists"] = os.path.exists(tesseract_path)
    
    return status
