"""
Vendor Notification API
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.notification_service import NotificationService
from pydantic import BaseModel
from typing import List
from datetime import datetime

router = APIRouter(prefix="/vendor/notifications", tags=["vendor-notifications"])

class NotificationSchema(BaseModel):
    id: int
    type: str
    message: str
    related_id: int | None
    is_read: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class MarkReadRequest(BaseModel):
    notification_id: int

@router.get("/", response_model=List[NotificationSchema])
def get_notifications(db: Session = Depends(get_db)):
    """Get unread notifications"""
    return NotificationService.get_unread(db)

@router.post("/read")
def mark_read(req: MarkReadRequest, db: Session = Depends(get_db)):
    """Mark notification as read"""
    success = NotificationService.mark_as_read(db, req.notification_id)
    return {"success": success}
