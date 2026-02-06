from pydantic import BaseModel, condecimal
from datetime import datetime
from uuid import UUID
from enum import Enum
from typing import Optional

class AdvanceRequestStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    PAID = "paid"

class AdvanceRequestCreate(BaseModel):
    invoice_id: UUID
    requested_amount: condecimal(max_digits=10, decimal_places=2)

class AdvanceRequestReview(BaseModel):
    status: AdvanceRequestStatus
    review_comment: Optional[str] = None

class AdvanceRequestResponse(BaseModel):
    advance_request_id: UUID
    invoice_id: UUID
    requested_amount: condecimal(max_digits=10, decimal_places=2)
    status: AdvanceRequestStatus
    reviewed_at: Optional[datetime]
    review_comment: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True
