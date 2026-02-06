from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from enum import Enum

class InvoiceStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    OVERDUE = "overdue"

class InvoiceStatusHistoryCreate(BaseModel):
    invoice_id: UUID
    previous_status: InvoiceStatus
    new_status: InvoiceStatus
    changed_by: str

class InvoiceStatusHistoryResponse(BaseModel):
    invoice_history_id: UUID
    invoice_id: UUID
    previous_status: InvoiceStatus
    new_status: InvoiceStatus
    changed_by: str
    changed_at: datetime

    class Config:
        orm_mode = True
