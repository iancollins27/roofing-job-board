# backend/app/models/job_model.py

from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, DateTime, Float, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base
from .company_model import Company  # Add this import
import enum

# Add this enum class after the imports
class JobFunction(str, enum.Enum):
    SALES = "sales"
    LABOR = "labor"
    PRODUCTION = "production"
    MANAGEMENT = "management"

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String, unique=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    job_title = Column(String, index=True)
    description = Column(Text)  # Make sure this is Text type to preserve HTML
    job_category = Column(Text)  # Store as JSON or comma-separated string
    location = Column(String)
    salary_range = Column(String, nullable=True)
    posted_date = Column(DateTime(timezone=True), server_default=func.now())  # Automatically set to now
    is_active = Column(Boolean, default=True)
    application_email = Column(String, nullable=True)
    application_link = Column(String, nullable=True)
    
    # New fields to match TheirStack data
    employment_type = Column(String)
    remote_type = Column(String)
    company_url = Column(String)
    source_url = Column(String)

    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    postal_code = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)

    job_function = Column(SQLAlchemyEnum(JobFunction), nullable=True)

    company = relationship("Company", back_populates="jobs")