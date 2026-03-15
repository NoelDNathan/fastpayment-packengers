from pydantic import BaseModel, condecimal, constr
from datetime import datetime
from typing import Optional
from enum import Enum
from uuid import UUID

<<<<<<< HEAD
# Payment status enum
class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    

class PaymentCreate(BaseModel):
=======
class InvoiceResponse(BaseModel):
    invoice_id: UUID
>>>>>>> 39bb7dbc7f8134f1a159c88d0fe34133b1731a0d
    account_id: UUID
    invoice_number: str
    issue_date: datetime
    due_date: datetime
    total_amount: float
    currency: str
    invoice_file_url: str
    created_at: datetime
    is_verified: bool


class InvoiceDownloadResponse(BaseModel):
    invoice_id: UUID
    download_url: str
    expires_in_seconds: int
