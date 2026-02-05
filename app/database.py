"""SQLAlchemy async configuration and lifecycle helpers."""

from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.config import settings


class Base(DeclarativeBase):
    """Declarative base for all SQLAlchemy models."""

    pass


def _make_async_url(url: str) -> str:
    """Normalize the configured DB URL to use asyncpg."""
    if url.startswith("postgresql+asyncpg://"):
        return url
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+asyncpg://", 1)
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    return url


ASYNC_DATABASE_URL: str = _make_async_url(settings.database_url)

# Engine and session factory
engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=settings.debug,
    future=True,
)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that yields an async SQLAlchemy session."""
    async with AsyncSessionLocal() as session:
        yield session


async def init_db() -> None:
    """Initialize database engine (connections are lazy)."""
    return None


async def close_db() -> None:
    """Dispose engine connections on shutdown."""
    await engine.dispose()
