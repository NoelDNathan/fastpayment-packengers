from pydantic import BaseModel, condecimal, constr
from datetime import datetime
from typing import Optional
from enum import Enum
from uuid import UUID

class InvoiceResponse(BaseModel):
    invoice_id: UUID
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
