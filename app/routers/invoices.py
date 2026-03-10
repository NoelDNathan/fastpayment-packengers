from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from uuid import UUID

from app.models.invoices import Invoice
from app.schemas.invoices import InvoiceDownloadResponse, InvoiceResponse
from app.database import get_db
from app.services.object_storage import ObjectStorageService

router = APIRouter(prefix="/invoices", tags=["Invoices"])
storage_service = ObjectStorageService()


# Get invoice by ID
@router.get("/{invoice_id}", response_model=InvoiceResponse)
async def get_invoice(invoice_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Invoice).filter(Invoice.invoice_id == invoice_id))
    invoice = result.scalars().one_or_none()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice


# Get all invoices (optional filter by account_id)
@router.get("/", response_model=List[InvoiceResponse])
async def get_all_invoices(
    account_id: Optional[UUID] = None, db: AsyncSession = Depends(get_db)
):
    stmt = select(Invoice)
    if account_id:
        stmt = stmt.filter(Invoice.account_id == account_id)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/{invoice_id}/download-url", response_model=InvoiceDownloadResponse)
async def get_invoice_download_url(
    invoice_id: UUID,
    expires_in_seconds: int = 900,
    db: AsyncSession = Depends(get_db),
):
    """Return a temporary signed URL to download an uploaded invoice file."""
    if expires_in_seconds < 60 or expires_in_seconds > 3600:
        raise HTTPException(
            status_code=400,
            detail="expires_in_seconds must be between 60 and 3600.",
        )

    result = await db.execute(select(Invoice).filter(Invoice.invoice_id == invoice_id))
    invoice = result.scalars().one_or_none()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    try:
        download_url = await storage_service.generate_download_url(
            invoice.invoice_file_url,
            expires_in_seconds=expires_in_seconds,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Could not generate invoice download URL.",
        ) from exc

    return InvoiceDownloadResponse(
        invoice_id=invoice.invoice_id,
        download_url=download_url,
        expires_in_seconds=expires_in_seconds,
    )
