"""
Main FastAPI application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db
from app.routes import customers, products, orders, invoices, dashboard, ai_agent, ocr, debug

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Production-ready backend for AI-powered SMB business automation with Natural Language Processing",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(customers.router, prefix=settings.API_V1_PREFIX)
app.include_router(products.router, prefix=settings.API_V1_PREFIX)
app.include_router(orders.router, prefix=settings.API_V1_PREFIX)
app.include_router(invoices.router, prefix=settings.API_V1_PREFIX)
app.include_router(dashboard.router, prefix=settings.API_V1_PREFIX)
app.include_router(ai_agent.router, prefix=settings.API_V1_PREFIX)
app.include_router(ocr.router, prefix=settings.API_V1_PREFIX)
app.include_router(debug.router, prefix=settings.API_V1_PREFIX)
from app.routes import customer_chat
app.include_router(customer_chat.router, prefix=settings.API_V1_PREFIX)
from app.routes import chat_onboarding
app.include_router(chat_onboarding.router, prefix=settings.API_V1_PREFIX)
from app.routes import vendor_notifications
app.include_router(vendor_notifications.router, prefix=settings.API_V1_PREFIX)


import asyncio
from app.database import SessionLocal
from app.services.product_service import ProductService

async def periodic_inventory_check():
    """Background task to check inventory levels periodically"""
    print("🕒 Periodic Inventory Check System Started (Every 10 mins)")
    while True:
        try:
            db = SessionLocal()
            try:
                products = ProductService.get_all_products(db, limit=1000)
                for p in products:
                    if p.stock_quantity <= p.reorder_threshold:
                         ProductService._trigger_low_stock_alert(db, p)
            finally:
                db.close()
        except Exception as e:
            print(f"Inventory check error: {e}")
            
        await asyncio.sleep(600) # 10 minutes

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    
    # Start background task
    asyncio.create_task(periodic_inventory_check())
    
    print("✅ Database initialized successfully")
    print(f"✅ {settings.APP_NAME} v{settings.APP_VERSION} is running")


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "SMB Business Automation API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "status": "running"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
