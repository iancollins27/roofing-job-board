from pydantic import BaseModel
from typing import Optional, List
from .user_schema import UserResponse
from .job_schema import JobResponse

class CompanyBase(BaseModel):
    name: str
    website: Optional[str] = None
    description: Optional[str] = None

class CompanyCreate(CompanyBase):
    pass

class CompanyResponse(CompanyBase):
    id: int
    is_active: bool
    users: Optional[List[UserResponse]] = []
    jobs: Optional[List[JobResponse]] = []

    class Config:
        from_attributes = True 