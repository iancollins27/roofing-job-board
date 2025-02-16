from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str  # In a real app, you'd want to hash this

class UserResponse(BaseModel):
    id: int
    email: str
    is_active: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str