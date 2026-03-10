from datetime import datetime
from pydantic import BaseModel, condecimal, constr
from typing import Optional

# -----------------------------
# Input when creating a payment
# -----------------------------
class PaymentCreate(BaseModel):
    id: int
    advance_request_id: Optional[int] = None  # payment may not be linked to invoice yet
    paid_amount: condecimal(max_digits=10, decimal_places=2)
    payment_method: constr(min_length=1, max_length=50)  # e.g., card, ACH, cash
    payment_date: datetime
    bank_reference: str
    payment_status: str

# -----------------------------
# Input for updating payment status
# -----------------------------
class PaymentStatusUpdate(BaseModel):
    payment_status: str  # e.g., pending, completed, failed

# -----------------------------
# Output when returning payment
# -----------------------------
class PaymentResponse(BaseModel):
    id: int
    advance_request_id: int
    bank_reference: str
    paid_amount: condecimal(max_digits=10, decimal_places=2)
    payment_method: str
    payment_date: datetime
    payment_status: str


    model_config = {
    "from_attributes": True
   }
