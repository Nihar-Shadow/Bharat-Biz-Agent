"""
Configuration settings for the application
"""
from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "SMB Business Automation API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "sqlite:///./smb_business.db"
    
    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent
    INVOICE_DIR: Path = BASE_DIR / "invoices"
    
    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()

# Ensure invoice directory exists
settings.INVOICE_DIR.mkdir(exist_ok=True)
