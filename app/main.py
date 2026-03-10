"""FastAPI application entry point."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import settings
from app.database import init_db, close_db
from app.middleware import setup_cors, setup_prometheus
from app.logging_config import setup_logging
from app.routers import health
<<<<<<< HEAD
from app.utils.third_party_auth import third_party_router



=======
from app.routers import accounts
from app.routers import advance_requests
from app.routers import invoice_status_history
from app.routers import invoices
from app.routers import payments
from app.routers import account_scores
>>>>>>> 39bb7dbc7f8134f1a159c88d0fe34133b1731a0d

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
<<<<<<< HEAD
app.include_router(third_party_router, prefix="/auth")  # now works
=======
app.include_router(accounts.router)
app.include_router(advance_requests.router)
app.include_router(invoice_status_history.router)
app.include_router(invoices.router)
app.include_router(payments.router)
app.include_router(account_scores.router)

>>>>>>> 39bb7dbc7f8134f1a159c88d0fe34133b1731a0d

@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint."""
    return {
        "message": "Fastpayment API",
        "version": "1.0.0",
        "docs": "/docs",
    }
