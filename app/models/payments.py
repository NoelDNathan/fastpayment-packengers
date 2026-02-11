import uuid
from enum import Enum
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Numeric, String, DateTime
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base


class PaymentStatus(str, Enum):
    ADVANCED = "advanced"
    RECOVERED = "recovered"
    PARTIAL_LOST = "partial_lost"
    LOST = "lost"


PaymentStatusEnum = SAEnum(PaymentStatus, name="payment_status")


class Payment(Base):
    __tablename__ = "payments"

    payment_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    advance_request_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    payment_status: Mapped[Optional[PaymentStatus]] = mapped_column(PaymentStatusEnum, nullable=True)
    paid_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    commission: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    payment_method: Mapped[str] = mapped_column(String, nullable=False)
    bank_reference: Mapped[str] = mapped_column(String, nullable=False)
    payment_date: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
