from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import orders, payments
from app.core.config import settings

app = FastAPI(
    title="Store API",
    description="A modern e-commerce store API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(orders.router, prefix="/api/v1", tags=["orders"])
app.include_router(payments.router, prefix="/api/v1", tags=["payments"])

@app.get("/")
async def root():
    return {"message": "Store API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
