"""
Notification Service
"""
from sqlalchemy.orm import Session
from app.models.notification import Notification
from typing import List

class NotificationService:
    @staticmethod
    def create_notification(db: Session, type: str, message: str, related_id: int = None):
        try:
            notif = Notification(
                type=type,
                message=message,
                related_id=related_id
            )
            db.add(notif)
            db.commit()
            return notif
        except Exception as e:
            print(f"Failed to create notification: {e}")
            db.rollback()
            return None

    @staticmethod
    def get_unread(db: Session, limit: int = 50) -> List[Notification]:
        return db.query(Notification).filter(Notification.is_read == False).order_by(Notification.created_at.desc()).limit(limit).all()

    @staticmethod
    def mark_as_read(db: Session, notification_id: int):
        notif = db.query(Notification).filter(Notification.id == notification_id).first()
        if notif:
            notif.is_read = True
            db.commit()
            return True
        return False
