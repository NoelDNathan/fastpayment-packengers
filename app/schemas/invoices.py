from pydantic import BaseModel, condecimal, constr
from datetime import datetime
from typing import Optional
from enum import Enum
from uuid import UUID

# Payment status enum
class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    

class PaymentCreate(BaseModel):
    account_id: UUID
    advance_request_id: Optional[UUID] = None
    paid_amount: condecimal(max_digits=10, decimal_places=2)
    payment_method: constr(min_length=1, max_length=50)
    payment_date: datetime
    bank_reference: constr(min_length=1)
    status: Optional[PaymentStatus] = PaymentStatus.PENDING  # default

class PaymentStatusUpdate(BaseModel):
    status: PaymentStatus

class PaymentResponse(BaseModel):
    payment_id: UUID
    account_id: UUID
    advance_request_id: Optional[UUID]
    paid_amount: condecimal(max_digits=10, decimal_places=2)
    payment_method: str
    payment_date: datetime
    bank_reference: str
    status: PaymentStatus
    created_at: datetime

    class Config:
        orm_mode = True


