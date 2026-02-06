import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from database import Base

class InvoiceStatusHistory(Base):
    __tablename__ = "invoice_status_history"

    invoice_history_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )

    invoice_id = Column(UUID(as_uuid=True), nullable=False)

    previous_status = Column(String, nullable=False)
    new_status = Column(String, nullable=False)

    changed_by = Column(String, nullable=False)  # user, system, admin, etc.

    changed_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
