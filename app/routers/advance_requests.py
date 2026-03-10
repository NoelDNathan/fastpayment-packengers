from datetime import datetime, timezone
import uuid
from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
import magic
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.advance_requests import AdvanceRequest, AdvanceInvoiceStatus
from app.models.invoice_status_history import (
    EntityType,
    EventType,
    InvoiceStatusHistory,
)
from app.models.invoices import Invoice
from app.schemas.advance_requests import (
    AdvanceSubmitData,
    AdvanceRequestCreate,
    AdvanceRequestResponse,
    AdvanceRequestReview,
    SubmitAdvanceRequestResponse,
)
from app.database import get_db
from app.services.object_storage import ObjectStorageService

router = APIRouter(prefix="/advance-requests", tags=["Advance Requests"])
storage_service = ObjectStorageService()
MAX_INVOICE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB
PDF_MIME_TYPE = "application/pdf"
FILE_SIGNATURE_READ_SIZE = 4096
SYSTEM_ACTOR_ID = uuid.UUID("00000000-0000-0000-0000-000000000000")


def detect_file_mime_type(upload_file: UploadFile) -> str:
    """Detect MIME type from file bytes using libmagic."""
    current_position = upload_file.file.tell()
    try:
        upload_file.file.seek(0)
        file_header = upload_file.file.read(FILE_SIGNATURE_READ_SIZE)
    finally:
        upload_file.file.seek(current_position)

    if not file_header:
        return ""
    return str(magic.from_buffer(file_header, mime=True))


# Create advance request
# @router.post("/", response_model=AdvanceRequestResponse)
# async def create_advance_request(
#     request: AdvanceRequestCreate, db: AsyncSession = Depends(get_db)
# ):
#     new_request = AdvanceRequest(
#     invoice_id=request.invoice_id,
#     requested_amount=request.requested_amount,
#     reviewed_by=None,
#     reviewed_at=None,
#     review_comment=None,
# )

#     db.add(new_request)
#     await db.commit()
#     await db.refresh(new_request)
#     return new_request


# Get one advance request
@router.get("/{advance_request_id}", response_model=AdvanceRequestResponse)
async def get_advance_request(
    advance_request_id: UUID, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(AdvanceRequest).filter(
            AdvanceRequest.advance_request_id == advance_request_id
        )
    )
    request = result.scalars().one_or_none()

    if not request:
        raise HTTPException(status_code=404, detail="Advance request not found")

    return request


# Review (approve / reject)
@router.patch("/{advance_request_id}/review", response_model=AdvanceRequestResponse)
async def review_advance_request(
    advance_request_id: UUID,
    review: AdvanceRequestReview,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(AdvanceRequest).filter(
            AdvanceRequest.advance_request_id == advance_request_id
        )
    )
    request = result.scalars().one_or_none()

    if not request:
        raise HTTPException(status_code=404, detail="Advance request not found")

    request.advance_request_status = review.status.value
    request.review_comment = review.review_comment
    request.reviewed_at = datetime.utcnow()

    await db.commit()
    await db.refresh(request)
    return request


@router.post(
    "/submit",
    response_model=SubmitAdvanceRequestResponse,
    status_code=status.HTTP_201_CREATED,
)
async def submit_advance_request(
    file: UploadFile = File(...),
    payload: AdvanceSubmitData = Depends(AdvanceSubmitData.as_form),
    db: AsyncSession = Depends(get_db),
):
    # 1) Validate file type and size
    filename = file.filename or ""
    if not filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are supported.",
        )

    detected_mime_type = detect_file_mime_type(file)
    if detected_mime_type != PDF_MIME_TYPE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file MIME type. Expected application/pdf content.",
        )

    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)

    if file_size <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty.",
        )

    if file_size > MAX_INVOICE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File exceeds the 10 MB size limit.",
        )

    existing_invoice_stmt = select(Invoice).where(
        Invoice.account_id == payload.account_id,
        Invoice.invoice_number == payload.invoice_number,
    )
    existing_invoice_result = await db.execute(existing_invoice_stmt)
    if existing_invoice_result.scalars().one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Invoice number already exists for this account.",
        )

    # 2) Upload to MinIO and collect object metadata
    created_object_key: str | None = None
    try:
        await storage_service.ensure_bucket_exists()
        invoice_id = uuid.uuid4()
        safe_filename = storage_service.sanitize_filename(filename)
        created_object_key = (
            f"invoices/{payload.account_id}/{invoice_id}_{safe_filename}"
        )
        invoice_file_url = await storage_service.upload_invoice(
            file.file,
            object_key=created_object_key,
            content_type="application/pdf",
        )

        # 3) Create Invoice with invoice_file_url
        new_invoice = Invoice(
            invoice_id=invoice_id,
            account_id=payload.account_id,
            invoice_number=payload.invoice_number,
            issue_date=payload.issue_date,
            due_date=payload.due_date,
            total_amount=payload.total_amount,
            currency=payload.currency,
            invoice_file_url=invoice_file_url,
            is_verified=False,
        )
        db.add(new_invoice)
        await db.flush()

        # 4) Create AdvanceRequest linked to invoice_id
        new_advance_request = AdvanceRequest(
            invoice_id=new_invoice.invoice_id,
            requested_amount=payload.requested_amount,
            reviewed_by=None,
            reviewed_at=None,
            review_comment=None,
        )
        db.add(new_advance_request)
        await db.flush()

        # Link entities so invoice can point to its originating request.
        new_invoice.advance_request_id = new_advance_request.advance_request_id

        # 5) Create status history events for both entities.
        invoice_uploaded_event = InvoiceStatusHistory(
            entity_type=EntityType.INVOICE,
            entity_id=new_invoice.invoice_id,
            previous_status=EventType.INVOICE_UPLOADED,
            new_status=EventType.INVOICE_UPLOADED,
            amount=payload.total_amount,
            changed_by=SYSTEM_ACTOR_ID,
        )
        advance_requested_event = InvoiceStatusHistory(
            entity_type=EntityType.ADVANCE_REQUEST,
            entity_id=new_advance_request.advance_request_id,
            previous_status=EventType.ADVANCE_REQUESTED,
            new_status=EventType.ADVANCE_REQUESTED,
            amount=payload.requested_amount,
            changed_by=SYSTEM_ACTOR_ID,
        )
        db.add(invoice_uploaded_event)
        db.add(advance_requested_event)
        await db.flush()

        # 6) Commit invoice, request, and history in one transaction.
        await db.commit()
        await db.refresh(new_invoice)
        await db.refresh(new_advance_request)

        return SubmitAdvanceRequestResponse(
            invoice_id=new_invoice.invoice_id,
            advance_request_id=new_advance_request.advance_request_id,
            invoice_file_url=new_invoice.invoice_file_url,
            advance_request_status=new_advance_request.advance_request_status.value,
            created_at=new_advance_request.created_at,
        )
    except Exception as exc:
        await db.rollback()
        # Compensating action: remove uploaded object if DB operation fails.
        if created_object_key is not None:
            try:
                await storage_service.delete_object(created_object_key)
            except Exception:
                pass
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to submit advance request.",
        ) from exc
    finally:
        await file.close()
