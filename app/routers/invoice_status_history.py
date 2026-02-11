from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID

from app.models.invoice_status_history import InvoiceStatusHistory, EntityType
from app.schemas.invoice_status_history import (
    InvoiceStatusHistoryCreate,
    InvoiceStatusHistoryResponse,
)
from app.database import get_db

router = APIRouter(prefix="/invoice-status-history", tags=["Invoice Status History"])


@router.post("/", response_model=InvoiceStatusHistoryResponse)
async def create_status_history(
    entry: InvoiceStatusHistoryCreate, db: AsyncSession = Depends(get_db)
):
    history = InvoiceStatusHistory(
        entity_type=EntityType.INVOICE,
        entity_id=entry.invoice_id,
        previous_status=entry.previous_status.value,
        new_status=entry.new_status.value,
        changed_by=entry.changed_by,
    )

    db.add(history)
    await db.commit()
    await db.refresh(history)
    return history


@router.get("/{invoice_id}", response_model=List[InvoiceStatusHistoryResponse])
async def get_invoice_history(invoice_id: UUID, db: AsyncSession = Depends(get_db)):
    stmt = (
        select(InvoiceStatusHistory)
        .filter(
            InvoiceStatusHistory.entity_type == EntityType.INVOICE,
            InvoiceStatusHistory.entity_id == invoice_id,
        )
        .order_by(InvoiceStatusHistory.changed_at)
    )
    result = await db.execute(stmt)
    rows = result.scalars().all()
    return rows

