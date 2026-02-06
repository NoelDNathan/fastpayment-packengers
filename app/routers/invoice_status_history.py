from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from models.invoice_status_history import InvoiceStatusHistory
from schemas.invoice_status_history import (
    InvoiceStatusHistoryCreate,
    InvoiceStatusHistoryResponse
)
from database import get_db

router = APIRouter(
    prefix="/invoice-status-history",
    tags=["Invoice Status History"]
)

# Add a status change record
@router.post("/", response_model=InvoiceStatusHistoryResponse)
def create_status_history(
    entry: InvoiceStatusHistoryCreate,
    db: Session = Depends(get_db)
):
    history = InvoiceStatusHistory(
        invoice_id=entry.invoice_id,
        previous_status=entry.previous_status.value,
        new_status=entry.new_status.value,
        changed_by=entry.changed_by
    )

    db.add(history)
    db.commit()
    db.refresh(history)
    return history


# Get full history for an invoice
@router.get("/{invoice_id}", response_model=List[InvoiceStatusHistoryResponse])
def get_invoice_history(invoice_id: UUID, db: Session = Depends(get_db)):
    return (
        db.query(InvoiceStatusHistory)
        .filter(InvoiceStatusHistory.invoice_id == invoice_id)
        .order_by(InvoiceStatusHistory.changed_at)
        .all()
    )
