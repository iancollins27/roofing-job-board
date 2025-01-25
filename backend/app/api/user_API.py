# backend/app/api/user_API.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.security import create_access_token, verify_password
from ..models.user_model import User
from ..schemas.user_schema import UserCreate, UserResponse, Token
from passlib.context import CryptContext

router = APIRouter()  # Ensure this line is present

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# backend/app/api/user_API.py

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = pwd_context.hash(user.password)  # Hash the password
    new_user = User(email=user.email, hashed_password=hashed_password)

    # If the user is associated with a company, set the company_id
    if user.company_id:  # Assuming UserCreate has a company_id field
        new_user.company_id = user.company_id

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/login", response_model=Token)
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}