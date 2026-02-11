import uuid
from enum import Enum
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, DateTime
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base


class RiskLevel(str, Enum):
    UNKWOWN = "unkwown"
    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    BLOCKED = "blocked"


RiskLevelEnum = SAEnum(RiskLevel, name="risk_level")


class AccountScore(Base):
    __tablename__ = "account_scores"

    account_score_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )

    account_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False)

    total_requests: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    approved_requests: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    rejected_requests: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    risk_level: Mapped[RiskLevel] = mapped_column(
        RiskLevelEnum, nullable=False, default=RiskLevel.UNKWOWN
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
