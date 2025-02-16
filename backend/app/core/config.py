# app/core/config.py

from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str
    
    # API settings
    THEIRSTACK_API_KEY: str
    THEIRSTACK_API_URL: str = "https://api.theirstack.com/v1/jobs/search"
    OPENAI_API_KEY: str
    STRIPE_SECRET_KEY: str
    GOOGLE_MAPS_API_KEY: str
    
    # JWT settings
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # API version
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Roofing Job Board"

    class Config:
        # This tells Pydantic to read from environment variables first
        env_file = None  # Disable .env file loading
        env_file_encoding = 'utf-8'

# Create an instance of Settings
settings = Settings()

# Validate required settings
if not settings.THEIRSTACK_API_KEY:
    raise ValueError("THEIRSTACK_API_KEY must be set in environment variables")
