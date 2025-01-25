# backend/app/models/user_model.py

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..core.database import Base
from .company_model import Company  # Add this import

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    
    # Foreign key for company association
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)  # Nullable for individual users
    company = relationship("Company", back_populates="users")  # Relationship to Company