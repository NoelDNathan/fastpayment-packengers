import uuid
from sqlalchemy import Column, String, Numeric, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from database import Base

class AdvanceRequest(Base):
    __tablename__ = "advance_requests"

    advance_request_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )

    invoice_id = Column(UUID(as_uuid=True), nullable=False)

    requested_amount = Column(Numeric(10, 2), nullable=False)

    status = Column(String, nullable=False, default="pending")
    # pending, approved, rejected, paid

    reviewed_at = Column(DateTime(timezone=True), nullable=True)

    review_comment = Column(String, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
