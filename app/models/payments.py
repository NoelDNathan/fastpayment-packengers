import uuid
from enum import Enum
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Numeric, String, DateTime
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
<<<<<<< HEAD
from database import Base
from sqlalchemy import Enum as SAEnum
from enum import Enum
=======
from app.database import Base


class PaymentStatus(str, Enum):
    ADVANCED = "advanced"
    RECOVERED = "recovered"
    PARTIAL_LOST = "partial_lost"
    LOST = "lost"
>>>>>>> 39bb7dbc7f8134f1a159c88d0fe34133b1731a0d


PaymentStatusEnum = SAEnum(PaymentStatus, name="payment_status")


class Payment(Base):
    __tablename__ = "payments"

    payment_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    advance_request_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    payment_status: Mapped[PaymentStatus] = mapped_column(PaymentStatusEnum, nullable=True)
    paid_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    commission: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    payment_method: Mapped[str] = mapped_column(String, nullable=False)
    bank_reference: Mapped[str] = mapped_column(String, nullable=False)
    payment_date: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    payment_document_url: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
