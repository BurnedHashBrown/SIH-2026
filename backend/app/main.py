import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config import settings
from app.database.database import engine, Base
from app.middleware.logging import RequestLoggingMiddleware
from app.middleware.error_handler import (
    http_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
)

# Configure standard root logger
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("metrology.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Ensure tables are created for SQLite / quickstart
    logger.info("Initializing database schema...")
    Base.metadata.create_all(bind=engine)
    logger.info("Application startup completed.")
    yield
    logger.info("Application shutting down...")


app = FastAPI(
    title=settings.APP_NAME,
    description="AI-Powered Legal Metrology Packaged Commodity Compliance System API for inspectors and regulatory verification.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/api/openapi.json",
)

# Exception Handlers
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Custom Middlewares
app.add_middleware(RequestLoggingMiddleware)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if isinstance(settings.CORS_ORIGINS, list) else [settings.CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.products import router as products_router
from app.api.inspections import router as inspections_router
from app.api.analysis import router as analysis_router
from app.api.reports import router as reports_router
from app.api.rules import router as rules_router
from app.api.dashboard import router as dashboard_router

# Include all API Routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(users_router, prefix=settings.API_V1_STR)
app.include_router(products_router, prefix=settings.API_V1_STR)
app.include_router(inspections_router, prefix=settings.API_V1_STR)
app.include_router(analysis_router, prefix=settings.API_V1_STR)
app.include_router(reports_router, prefix=settings.API_V1_STR)
app.include_router(rules_router, prefix=settings.API_V1_STR)
app.include_router(dashboard_router, prefix=settings.API_V1_STR)


@app.get(
    f"{settings.API_V1_STR}/health",
    tags=["System"],
    summary="Health check endpoint",
    response_model=dict,
    status_code=status.HTTP_200_OK,
)
def health_check():
    """Returns application health status."""
    return {"status": "ok"}


