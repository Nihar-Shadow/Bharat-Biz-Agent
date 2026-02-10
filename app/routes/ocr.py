"""
OCR Bill Upload Routes
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
from app.services.ocr_service import ocr_processor

router = APIRouter(prefix="/ocr", tags=["ocr"])


@router.post("/upload-bill")
async def upload_bill(file: UploadFile = File(...)):
    """
    Upload a bill image and extract product information using OCR
    
    - **file**: Bill image (JPG, PNG, etc.)
    
    Returns:
    - Extracted text
    - List of items with product name, quantity, and price
    - Total amount
    """
    # Validate file type
    allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed types: {', '.join(allowed_types)}"
        )
    
    # Read file
    try:
        contents = await file.read()
        
        # Process with OCR
        result = ocr_processor.process_bill_image(contents)
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result.get("error", "OCR processing failed"))
        
        return JSONResponse(content=result)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process image: {str(e)}")


@router.post("/extract-text")
async def extract_text_only(file: UploadFile = File(...)):
    """
    Extract raw text from bill image (no parsing)
    
    - **file**: Bill image
    
    Returns:
    - Raw extracted text
    """
    allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed types: {', '.join(allowed_types)}"
        )
    
    try:
        contents = await file.read()
        text = ocr_processor.extract_text_from_image(contents)
        
        return {
            "success": True,
            "text": text,
            "message": "Text extracted successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text extraction failed: {str(e)}")
