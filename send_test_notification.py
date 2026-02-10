
from app.database import SessionLocal
from app.services.notification_service import NotificationService

db = SessionLocal()
try:
    print("Creating test notification...")
    NotificationService.create_notification(
        db, 
        "SYSTEM_TEST", 
        "This is a test notification from the system to verify alerts are working.", 
        0
    )
    print("✅ Test notification created.")
except Exception as e:
    print(f"❌ Failed: {e}")
finally:
    db.close()
