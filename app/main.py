"""FastAPI application entry point."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import settings
from app.database import init_db, close_db
from app.middleware import setup_cors, setup_prometheus
from app.logging_config import setup_logging
from app.routers import health
from app.utils.third_party_auth import third_party_router




# Setup logging
setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    await init_db()
    yield
    # Shutdown
    await close_db()


# Create FastAPI app
app = FastAPI(
    title="Fastpayment API",
    description="FastAPI backend for Fastpayment",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
#
)
# Setup logging
setup_logging()

# Setup middleware
setup_cors(app)
setup_prometheus(app)

# Include routers
app.include_router(health.router)
app.include_router(third_party_router, prefix="/auth")  # now works

@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint."""
    return {
        "message": "Fastpayment API",
        "version": "1.0.0",
        "docs": "/docs",
    }
