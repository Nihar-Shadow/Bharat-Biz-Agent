"""
AI Agent API routes
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.ai_action_router import AIActionRouter
from pydantic import BaseModel
from typing import Dict, Any

router = APIRouter(prefix="/ai", tags=["ai-agent"])


class MessageInput(BaseModel):
    """Input schema for AI agent"""
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Order 2 laptops for Rahul"
            }
        }


class AIResponse(BaseModel):
    """Response schema for AI agent"""
    intent: str
    confidence: float
    entities: Dict[str, Any]
    action_result: Dict[str, Any]
    original_message: str


@router.post("/process", response_model=AIResponse)
def process_natural_language(
    input_data: MessageInput,
    db: Session = Depends(get_db)
):
    """
    Process natural language message and execute backend action
    
    Supports:
    - English, Hindi, and Hinglish
    - Spelling error tolerance
    - Multiple intents (create_order, check_inventory, generate_invoice, etc.)
    
    Examples:
    - "Order 2 laptops for Rahul"
    - "Laptop chahiye 2 pieces for Rahul"
    - "Check stock of mouse"
    - "Kitne laptop available hai?"
    - "Generate bill for order 123"
    - "Invoice dedo order #5 ka"
    - "Add customer Priya phone 9876543210"
    - "Payment reminder for Amit"
    """
    router_instance = AIActionRouter(db)
    result = router_instance.process_message(input_data.message)
    return result


@router.get("/test")
def test_ai_agent():
    """
    Test endpoint to verify AI agent is working
    """
    return {
        "status": "active",
        "message": "AI Agent Engine is running",
        "supported_intents": [
            "create_order",
            "check_inventory",
            "generate_invoice",
            "add_customer",
            "payment_reminder_suggestion"
        ],
        "supported_languages": ["English", "Hindi", "Hinglish"],
        "features": [
            "Intent detection",
            "Entity extraction",
            "Fuzzy matching for spelling errors",
            "Hinglish support",
            "Action routing",
            "AI action logging"
        ]
    }


@router.post("/test-intent")
def test_intent_detection(input_data: MessageInput):
    """
    Test intent detection without executing actions
    
    Use this to see what intent and entities are detected
    without actually creating orders, etc.
    """
    from app.services.ai_agent_engine import AIAgentEngine
    
    engine = AIAgentEngine()
    intent = engine.detect_intent(input_data.message)
    
    return engine.to_json(intent)
