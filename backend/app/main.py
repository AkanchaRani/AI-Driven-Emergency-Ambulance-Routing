"""
FastAPI entry point.  Run from the backend folder:

    uvicorn app.main:app --reload
"""
import logging

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.config import settings
from app.database.connection import get_db
from app.routers import emergencies, resources

logger = logging.getLogger("ambulance_routing")

app = FastAPI(
    title="AI-Driven Emergency Ambulance Routing System",
    description="Backend API - emergency requests, ambulances and hospitals.",
    version="0.1.0",
)

# CORS: lets the React app (a different port) call this API from the browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(emergencies.router)
app.include_router(resources.router)


@app.exception_handler(SQLAlchemyError)
async def database_error_handler(request: Request, exc: SQLAlchemyError):
    # Full error goes to the server console; the browser gets a short message
    logger.exception("Database error on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "Database error. Check that MySQL is running and the .env settings are correct."},
    )


@app.get("/api/health", tags=["System"])
def health_check(db: Session = Depends(get_db)):
    """Returns 200 when the API is running and MySQL answers a simple query."""
    db.execute(text("SELECT 1"))
    return {"status": "ok", "database": "connected", "service": "ambulance-routing-api"}
