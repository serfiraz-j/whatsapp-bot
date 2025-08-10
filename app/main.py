import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from loguru import logger

from app.config import settings
from app.database import create_db_and_tables
from app.routers import auth, chat, clinic
from app.admin import dashboard

# Configure Loguru to intercept standard logging
class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        logger.log(level, record.getMessage())

logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup
    logger.info("Starting up application...")
    logger.info(f"Connecting to database at {settings.DATABASE_URL}")
    await create_db_and_tables()
    logger.info("Database tables created.")
    yield
    # On shutdown
    logger.info("Shutting down application...")


app = FastAPI(
    title="AI Clinic Assistant",
    description="A production-ready backend for an AI-powered WhatsApp assistant for clinics.",
    version="1.0.0",
    lifespan=lifespan
)

# --- Routers ---
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(clinic.router, prefix="/clinic", tags=["Clinic Management"])
app.include_router(chat.router, prefix="/chat", tags=["Chat & WhatsApp"])
app.include_router(dashboard.router, prefix="/admin", tags=["Admin"])


# --- Health Check Endpoint ---
@app.get("/health", status_code=status.HTTP_200_OK, tags=["Health"])
async def health_check():
    """
    Health check endpoint to ensure the service is running.
    """
    return {"status": "ok"}

# --- Exception Handler ---
@app.exception_handler(Exception)
async def validation_exception_handler(request: Request, exc: Exception):
    logger.error(f"An unhandled exception occurred: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal server error occurred."},
    )