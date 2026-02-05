import datetime
from pydantic import BaseModel, condecimal, constr
from typing import Optional

# -----------------------------
# Input when creating a payment
# -----------------------------
class PaymentCreate(BaseModel):
    id: int
    advance_request_id: Optional[int] = None  # payment may not be linked to invoice yet
    paid_amount: condecimal(max_digits=10, decimal_places=2)
    payment_method: str(min_length=1, max_length=50)  # e.g., card, ACH, cash
    payment_date: datetime
    bank_reference: str
    status: str

# -----------------------------
# Input for updating payment status
# -----------------------------
class PaymentStatusUpdate(BaseModel):
    status: str  # e.g., pending, completed, failed

# -----------------------------
# Output when returning payment
# -----------------------------
class PaymentResponse(BaseModel):
    id: int
    advance_request_id: int
    bank_reference: [int]
    paid_amount: condecimal(max_digits=10, decimal_places=2)
    payment_method: str
    payment_date: datetime
    status: str


    class Config:
        orm_mode = True  # allows SQLAlchemy models to be returned directly
