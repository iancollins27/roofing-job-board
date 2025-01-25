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

class JobResponse(JobCreate):
    id: Optional[int] = None
    posted_date: Optional[Union[datetime, str]] = None  # Allow both datetime and string
    is_active: Optional[bool] = None
    postal_code: Optional[str] = None  # Make it optional in responses

    class Config:
        orm_mode = True
        from_attributes = True  # For newer Pydantic versions