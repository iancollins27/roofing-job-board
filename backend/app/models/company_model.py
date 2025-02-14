from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from ..core.database import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    website = Column(String, nullable=True)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    # users = relationship("User", back_populates="company")  # Commented out until User model is needed
    jobs = relationship("Job", back_populates="company") 