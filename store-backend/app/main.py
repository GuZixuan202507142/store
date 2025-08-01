from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import payments, ai
from app.db.session import init_db
from app.core.config import settings

app = FastAPI(
    title="Copilot Store API",
    description="API for selling GitHub Copilot Education Edition accounts.",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],  # Restrict to frontend URL
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    await init_db()

# Include API routers
app.include_router(payments.router, prefix="/api/v1/payments", tags=["Payments"])
app.include_router(ai.router, prefix="/api/v1/ai", tags=["AI"])

@app.get("/health")
def health_check():
    return {"status": "ok"}
