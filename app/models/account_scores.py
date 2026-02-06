import uuid
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from database import Base

class AccountScore(Base):
    __tablename__ = "account_scores"

    account_score_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )

    account_id = Column(UUID(as_uuid=True), nullable=False, unique=True)

    total_requests = Column(Integer, nullable=False, default=0)
    approved_requests = Column(Integer, nullable=False, default=0)
    rejected_requests = Column(Integer, nullable=False, default=0)

    risk_level = Column(String, nullable=False)  # low, medium, high

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
