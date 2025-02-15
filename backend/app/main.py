# backend/app/main.py

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .api import user_API, job_API, company_API, payment_API  # Add payment_API
from .core.database import init_db, engine, Base
from contextlib import asynccontextmanager

# Remove these lines that drop and recreate tables
# Base.metadata.drop_all(bind=engine)
# Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  # This will create tables if they don't exist
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include the user and job routers
app.include_router(user_API.router, prefix="/api/v1/users", tags=["users"])
app.include_router(job_API.router, prefix="/api/v1/jobs", tags=["jobs"])
app.include_router(company_API.router, prefix="/api/v1/companies", tags=["companies"])
app.include_router(payment_API.router, prefix="/api/v1/payments", tags=["payments"])

# Basic test route
@app.get("/")
async def root():
    return {"message": "Welcome to the Roofing Job Board API"}