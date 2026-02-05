from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from models.invoices import Invoice
from schemas.invoices import InvoiceCreate, InvoiceResponse, InvoiceStatus
from database import get_db

router = APIRouter(
    prefix="/invoices",
    tags=["Invoices"]
)

# Create invoice
@router.post("/", response_model=InvoiceResponse)
def create_invoice(invoice: InvoiceCreate, db: Session = Depends(get_db)):
    new_invoice = Invoice(
        account_id=invoice.account_id,
        invoice_number=invoice.invoice_number,
        issue_date=invoice.issue_date,
        due_date=invoice.due_date,
        total_amount=invoice.total_amount,
        currency=invoice.currency,
        invoice_file_url=invoice.invoice_file_url,
        invoice_status=invoice.invoice_status.value
    )

    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)
    return new_invoice


# Get invoice by ID
@router.get("/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(invoice_id: UUID, db: Session = Depends(get_db)):
    invoice = db.query(Invoice).filter(Invoice.invoice_id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice


# Get all invoices (optional filter by account_id)
@router.get("/", response_model=List[InvoiceResponse])
def get_all_invoices(account_id: Optional[UUID] = None, db: Session = Depends(get_db)):
    query = db.query(Invoice)
    if account_id:
        query = query.filter(Invoice.account_id == account_id)
    return query.all()


# Update invoice status
@router.patch("/{invoice_id}/status", response_model=InvoiceResponse)
def update_invoice_status(invoice_id: UUID, status: InvoiceStatus, db: Session = Depends(get_db)):
    invoice = db.query(Invoice).filter(Invoice.invoice_id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    invoice.invoice_status = status.value
    db.commit()
    db.refresh(invoice)
    return invoice
