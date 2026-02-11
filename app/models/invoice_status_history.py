import uuid
from enum import Enum
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, Numeric, BigInteger
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base


class EntityType(str, Enum):
    INVOICE = "invoice"
    ADVANCE_REQUEST = "advance_request"
    PAYMENT = "payment"


class EventType(str, Enum):
    INVOICE_UPLOADED = "invoice_uploaded"
    ADVANCE_REQUESTED = "advance_requested"
    ADVANCE_APPROVED = "advance_approved"
    ADVANCE_REJECTED = "advance_rejected"
    MONEY_RECOVERED = "money_recovered"
    MONEY_LOST = "money_lost"
    MONEY_PARTIAL_LOST = "money_partial_lost"


class RiskLevel(str, Enum):
    UNKWOWN = "unkwown"
    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    BLOCKED = "blocked"


EntityTypeEnum = SAEnum(EntityType, name="entity_type")
EventTypeEnum = SAEnum(EventType, name="event_type")
RiskLevelEnum = SAEnum(RiskLevel, name="risk_level")


class InvoiceStatusHistory(Base):
    __tablename__ = "events_history"

    event_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )

    entity_type: Mapped[EntityType] = mapped_column(EntityTypeEnum, nullable=False)

    entity_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False)

    previous_status: Mapped[EventType] = mapped_column(EventTypeEnum, nullable=False)
    new_status: Mapped[EventType] = mapped_column(EventTypeEnum, nullable=False)

    amount: Mapped[Optional[float]] = mapped_column(Numeric(10, 2), nullable=True)
    event_metadata: Mapped[Optional[int]] = mapped_column(
        "metadata", BigInteger, nullable=True
    )

    changed_by: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False)

    changed_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    score_changed: Mapped[Optional[RiskLevel]] = mapped_column(
        RiskLevelEnum, nullable=True
    )
