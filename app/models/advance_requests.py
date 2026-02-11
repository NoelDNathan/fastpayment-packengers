import uuid
from enum import Enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Numeric, DateTime, text
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base


class AdvanceInvoiceStatus(str, Enum):
    REQUESTED = "requested"
    PARTIAL_APPROVED = "partial_approved"
    APPROVED = "approved"
    REJECTED = "rejected"


AdvanceInvoiceStatusEnum = SAEnum(AdvanceInvoiceStatus, name="advance_invoice_status")


class AdvanceRequest(Base):
    __tablename__ = "advance_invoices"

    advance_request_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )

    invoice_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False)

    requested_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    reviewed_by: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=True)

    advance_request_status: Mapped[AdvanceInvoiceStatus] = mapped_column(
        AdvanceInvoiceStatusEnum, nullable=False, default=AdvanceInvoiceStatus.REQUESTED
    )

    reviewed_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    review_comment: Mapped[str] = mapped_column(String, nullable=True)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
