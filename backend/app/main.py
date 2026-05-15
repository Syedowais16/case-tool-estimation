"""FastAPI main application"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
from app.core.config.settings import get_settings
from app.api.v1.router import api_router
from app.db.base import init_db, engine
from app.middleware.logging_middleware import LoggingMiddleware

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     """Application lifespan context manager"""
#     # Startup
#     logger.info("Starting CASE Tool API...")
#     init_db()
#     logger.info("Database initialized")
    
#     yield
    
#     # Shutdown
#     logger.info("Shutting down CASE Tool API...")
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting CASE Tool API...")

    init_db()
    logger.info("Database initialized")

    # 🔥 ADD THIS LINE
    from app.db.seed_data import seed_database
    seed_database()

    logger.info("Database seeded successfully")

    yield

    logger.info("Shutting down CASE Tool API...")

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description=settings.api_description,
    version=settings.app_version,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_credentials,
    allow_methods=settings.cors_methods,
    allow_headers=settings.cors_headers,
)

# Add TrustedHost middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]
)

# Add custom logging middleware
app.add_middleware(LoggingMiddleware)

# Include API router
app.include_router(api_router)


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.app_version,
        "environment": settings.environment
    }


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "api_docs": "/docs"
    }


# Exception handlers
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.server_host,
        port=settings.server_port,
        workers=settings.workers if settings.environment == "production" else 1,
        log_level=settings.log_level.lower()
    )
