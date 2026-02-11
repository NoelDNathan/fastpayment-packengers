import uuid
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Numeric, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base


class Invoice(Base):
    __tablename__ = "invoices"

    invoice_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    account_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    advance_request_id: Mapped[Optional[UUID]] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )
    invoice_number: Mapped[str] = mapped_column(String, nullable=False)
    issue_date: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    due_date: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    total_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String, nullable=False)
    invoice_file_url: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
