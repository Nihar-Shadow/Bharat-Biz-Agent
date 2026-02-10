"""
AI Action Log database model
"""
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.database import Base


class AIActionLog(Base):
    """AI Action Log model for tracking AI-powered actions"""
    
    __tablename__ = "ai_actions_log"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    action_type = Column(String(100), nullable=False, index=True)
    input_text = Column(Text, nullable=True)
    output_action = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    def __repr__(self):
        return f"<AIActionLog(id={self.id}, type='{self.action_type}', time={self.timestamp})>"
