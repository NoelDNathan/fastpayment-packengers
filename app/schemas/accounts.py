"""Pydantic schemas for Account model."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID
from typing import Any

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.types import AccountType

class AccountsSchema(BaseModel):


class AccountBase(BaseModel):
    """Shared fields for accounts."""

    role: AccountType
    email: EmailStr
    name: str = Field(min_length=1)
    last_name: str | None = None
    avatar_url: str | None = None
    bases_positions: list[PositionSchema] | None = None


class AccountCreate(AccountBase):
    """Payload for creating an account."""

    password: str = Field(min_length=8, description="Password must be at least 8 characters")


class AccountUpdate(BaseModel):
    """Partial update for accounts."""

    role: AccountType | None = None
    email: EmailStr | None = None
    name: str | None = Field(None, min_length=1)
    last_name: str | None = None
    avatar_url: str | None = None
    bases_positions: list[PositionSchema] | None = None
    is_active: bool | None = None
    is_verified: bool | None = None
    documents_verified: bool | None = None


class AccountResponse(AccountBase):
    """Response schema for accounts."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    role: AccountType
    email: EmailStr
    name: str
    last_name: str | None = None
    is_active: bool
    is_verified: bool
    documents_verified: bool
    avatar_url: str | None = None
    bases_positions: list[PositionSchema] | None = None
    created_at: datetime
    updated_at: datetime


class AccountPublic(AccountBase):
    """Public response schema for accounts (without sensitive fields)."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    is_active: bool
    is_verified: bool
    documents_verified: bool
    avatar_url: str | None = None
    created_at: datetime
    updated_at: datetime


class FleetSizeResponse(BaseModel):
    """Response schema for fleet size."""

    fleet_size: int
    account_id: UUID