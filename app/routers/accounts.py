"""Accounts documents router."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_current_active_user, get_db
from app.models.account import Account
from app.models.accounts_documents import AccountsDocuments
from app.schemas.accounts_documents import (
    AccountsDocumentsCreate,
    AccountsDocumentsResponse,
    AccountsDocumentsUpdate,
)

router = APIRouter(prefix="/api/accounts", tags=["accounts"])





@router.get("/{account_id}", response_model=AccountsDocumentsResponse)
async def get_account(
    account_id: UUID,
    session: AsyncSession = Depends(get_db),
) -> AccountsDocumentsResponse:
    """Get a specific document by ID."""
    account = await session.get(Account, account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found",
        )

        

    return AccountsDocumentsResponse.model_validate(document)


@router.post("", response_model=AccountsDocumentsResponse, status_code=status.HTTP_201_CREATED)
async def create_document(
    document_data: AccountsDocumentsCreate,
    current_user: Account = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_db),
) -> AccountsDocumentsResponse:
    """Create a new document."""
    # Ensure the account_id matches the current user
    if document_data.account_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot create document for another user",
        )

    payload = document_data.model_dump(exclude_unset=True)
    document = AccountsDocuments(**payload)
    session.add(document)
    await session.commit()
    await session.refresh(document)
    return AccountsDocumentsResponse.model_validate(document)


@router.put("/{document_id}", response_model=AccountsDocumentsResponse)
async def update_document(
    document_id: UUID,
    document_update: AccountsDocumentsUpdate,
    current_user: Account = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_db),
) -> AccountsDocumentsResponse:
    """Update a document."""
    document = await session.get(AccountsDocuments, document_id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    if document.account_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    # Prevent changing account_id to another user
    update_data = document_update.model_dump(exclude_unset=True)
    if "account_id" in update_data and update_data["account_id"] != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot transfer document to another user",
        )

    for field, value in update_data.items():
        setattr(document, field, value)

    await session.commit()
    await session.refresh(document)
    return AccountsDocumentsResponse.model_validate(document)


@router.delete("/{document_id}")
async def delete_document(
    document_id: UUID,
    current_user: Account = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    """Delete a document."""
    document = await session.get(AccountsDocuments, document_id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    if document.account_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    await session.delete(document)
    await session.commit()
    return {"message": "Document deleted successfully"}
