"""Accounts router."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/api/accounts", tags=["accounts"])


@router.get("/{account_id}")
async def get_account(
    account_id: UUID,
) -> dict[str, str]:
    """Placeholder endpoint until accounts module is implemented."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail=f"Accounts endpoint not implemented yet for account_id={account_id}",
    )


@router.get("")
async def list_accounts() -> dict[str, str]:
    """Placeholder endpoint until accounts module is implemented."""
    return {"message": "Accounts endpoint not implemented yet"}
