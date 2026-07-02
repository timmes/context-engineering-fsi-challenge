"""Open Banking API — PSD2-compliant payment services."""

from fastapi import FastAPI
from mangum import Mangum

from src.middleware.audit import AuditMiddleware
from src.routes.payments import router as payments_router

app = FastAPI(
    title="Open Banking API",
    version="1.0.0",
    description="PSD2-compliant payment initiation service",
)

# Middleware
app.add_middleware(AuditMiddleware)

# Routes
app.include_router(payments_router, prefix="/v1")


# AWS Lambda handler
handler = Mangum(app)

@app.get("/health")
async def health_check():
    """Health check endpoint — no auth required."""
    return {"status": "healthy", "service": "open-banking-api"}
