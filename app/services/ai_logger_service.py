"""
AI Logger service - business logic for AI action logging
"""
from sqlalchemy.orm import Session
from app.models.ai_action import AIActionLog
from typing import List, Optional


class AILoggerService:
    """Service class for AI action logging"""
    
    @staticmethod
    def log_action(
        db: Session,
        action_type: str,
        input_text: Optional[str] = None,
        output_action: Optional[str] = None
    ) -> AIActionLog:
        """Log an AI action"""
        log_entry = AIActionLog(
            action_type=action_type,
            input_text=input_text,
            output_action=output_action
        )
        db.add(log_entry)
        db.commit()
        db.refresh(log_entry)
        return log_entry
    
    @staticmethod
    def get_logs(db: Session, skip: int = 0, limit: int = 100) -> List[AIActionLog]:
        """Get AI action logs with pagination"""
        return db.query(AIActionLog).order_by(
            AIActionLog.timestamp.desc()
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_logs_by_type(db: Session, action_type: str) -> List[AIActionLog]:
        """Get AI action logs filtered by type"""
        return db.query(AIActionLog).filter(
            AIActionLog.action_type == action_type
        ).order_by(AIActionLog.timestamp.desc()).all()
