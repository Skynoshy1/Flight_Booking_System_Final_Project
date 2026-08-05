"""
Application Configuration
Centralized configuration management using environment variables
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    # Application
    APP_NAME: str = "Traveloka Flight Booking API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    
    # CORS
    CORS_ORIGINS: list = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "https://skynoshy1.github.io"
    ]
    
    # Database
    DATABASE_URL: str = "sqlite:///./traveloka_flights.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # External APIs
    CURRENCY_API_KEY: Optional[str] = None
    CURRENCY_API_URL: str = "https://api.exchangerate-api.com/v4/latest"
    
    # Seat Locking
    SEAT_LOCK_TIMEOUT_SECONDS: int = 300  # 5 minutes
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
