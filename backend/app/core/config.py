# app/core/config.py

from pydantic_settings import BaseSettings
from pathlib import Path
from dotenv import load_dotenv
import os

# Get the absolute path to the backend directory and load environment
BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BACKEND_DIR / '.env'

print(f"Looking for .env at: {ENV_PATH}")
if not ENV_PATH.exists():
    raise FileNotFoundError(f".env file not found at {ENV_PATH}")

load_dotenv(ENV_PATH)

# Debug database connection
db_url = os.getenv('DATABASE_URL', '')
if db_url and db_url.startswith('postgres://'):
    db_url = db_url.replace('postgres://', 'postgresql://', 1)

print("\nDatabase Connection Debug:")
print(f"1. Found DATABASE_URL in env: {'Yes' if db_url else 'No'}")
if db_url:
    parts = db_url.split('@')[0].split(':')
    user = parts[1].replace('//', '')
    print(f"2. Username: {user}")
    print(f"3. Host: {db_url.split('@')[1].split('/')[0]}")
    print(f"4. Database: {db_url.split('/')[-1]}")

# Verify key environment variables after loading
if not os.getenv('THEIRSTACK_API_KEY'):
    raise ValueError("THEIRSTACK_API_KEY not found in environment variables")

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = db_url
    
    # API settings
    THEIRSTACK_API_KEY: str = os.getenv('THEIRSTACK_API_KEY')
    THEIRSTACK_API_URL: str = "https://api.theirstack.com/v1/jobs/search"
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY', '')
    STRIPE_SECRET_KEY: str = os.getenv('STRIPE_SECRET_KEY', '')
    GOOGLE_MAPS_API_KEY: str = os.getenv('GOOGLE_MAPS_API_KEY', '')
    
    # JWT settings
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # API version
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Roofing Job Board"

    def __init__(self, **kwargs):
        print(f"Loading env from: {ENV_PATH}")
        print(f"Env file exists: {ENV_PATH.exists()}")
        if ENV_PATH.exists():
            with open(ENV_PATH, 'r') as f:
                print("Found .env file with contents:")
                for line in f:
                    if line.strip() and not line.startswith('#'):
                        key = line.split('=')[0]
                        print(f"{key}=***")
        super().__init__(**kwargs)

settings = Settings()

# Validate required settings
if not settings.THEIRSTACK_API_KEY:
    raise ValueError("THEIRSTACK_API_KEY must be set in .env file")