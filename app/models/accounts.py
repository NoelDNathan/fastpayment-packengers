"""Account model replacing user and profile."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum
from sqlalchemy import Enum as SAEnum
from app.database import Base
from app.models.types import AccountTypeEnum, PositionType


class AccountStatus(str, Enum): 
    ACTIVE = "active"
    SUSPENDED = "suspended"

AccountStatusEnum = SAEnum(AccountStatus, name="account_status")

class Account(Base):
    """Unified account entity (users and profiles)."""

    __tablename__ = "account"

    account_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    phone: Mapped[str] = mapped_column(String(15), nullable=False)
    email: Mapped[str] = mapped_column(String(55), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    tax_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    iban: Mapped[str] = mapped_column(String(255), nullable=False)
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[AccountStatusEnum] = mapped_column(AccountStatusEnum, default=AccountStatus.ACTIVE, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)
       
    

    def __repr__(self) -> str:
        return f"Account(email={self.email})"