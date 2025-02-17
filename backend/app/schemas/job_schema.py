# backend/app/schemas/job_schema.py

from pydantic import BaseModel, validator
from typing import Optional, List, Union
from datetime import datetime
from enum import Enum

class JobFunction(str, Enum):
    SALES = "sales"
    LABOR = "labor"
    PRODUCTION = "production"
    MANAGEMENT = "management"
    OTHER = "other"  # Added for backward compatibility

class JobCreate(BaseModel):
    external_id: Optional[str] = None
    company_id: Optional[int] = None
    job_title: str
    description: str
    location: str
    postal_code: str  # Required field
    employment_type: Optional[str] = None
    remote_type: Optional[str] = None
    salary_range: Optional[str] = None
    application_email: Optional[str] = None
    application_link: Optional[str] = None
    company_url: Optional[str] = None
    job_function: Optional[JobFunction] = None

    @validator('postal_code')
    def validate_postal_code(cls, v):
        if v is None:  # Allow None values
            return v
        if not v.isdigit() or len(v) != 5:
            raise ValueError('ZIP code must be 5 digits')
        return v

class JobResponse(BaseModel):
    id: Optional[int] = None
    external_id: Optional[str] = None
    company_id: Optional[int] = None
    job_title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    postal_code: Optional[str] = None
    employment_type: Optional[str] = None
    remote_type: Optional[str] = None
    salary_range: Optional[str] = None
    application_email: Optional[str] = None
    application_link: Optional[str] = None
    company_url: Optional[str] = None
    source_url: Optional[str] = None
    job_function: Optional[str] = None  # Changed from JobFunction to str to be more lenient
    posted_date: Optional[Union[datetime, str]] = None
    is_active: Optional[bool] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    city: Optional[str] = None
    state: Optional[str] = None

    class Config:
        from_attributes = True
        # Allow extra fields in case database has fields not in schema
        extra = "allow"

class PaginatedJobResponse(BaseModel):
    items: List[JobResponse]
    total: int
    skip: int
    limit: int

    class Config:
        from_attributes = True