# app/core/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
import os

# Debug connection string
db_url = settings.DATABASE_URL
print(f"\nAttempting database connection with URL format: {db_url.split(':')[0]}://{db_url.split(':')[1].split('@')[0].split(':')[0]}:***@{db_url.split('@')[1]}")

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=True  # This will log all SQL commands
)

# Create SessionLocal class for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for database models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Add this new function
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Create database tables"""
    Base.metadata.create_all(bind=engine)