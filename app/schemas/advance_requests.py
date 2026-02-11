from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional
from uuid import UUID

from fastapi import Form
from pydantic import BaseModel, ConfigDict, condecimal


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

    model_config = ConfigDict(from_attributes=True)


class SubmitAdvanceRequestResponse(BaseModel):
    invoice_id: UUID
    advance_request_id: UUID
    invoice_file_url: str
    advance_request_status: str
    created_at: datetime


class AdvanceSubmitData(BaseModel):
    account_id: UUID
    invoice_number: str
    issue_date: datetime
    due_date: datetime
    total_amount: Decimal
    currency: str
    requested_amount: Decimal

    @classmethod
    def as_form(
        cls,
        account_id: UUID = Form(...),
        invoice_number: str = Form(...),
        issue_date: datetime = Form(...),
        due_date: datetime = Form(...),
        total_amount: Decimal = Form(...),
        currency: str = Form(...),
        requested_amount: Decimal = Form(...),
    ) -> "AdvanceSubmitData":
        """Build Pydantic model from multipart form fields."""
        return cls(
            account_id=account_id,
            invoice_number=invoice_number,
            issue_date=issue_date,
            due_date=due_date,
            total_amount=total_amount,
            currency=currency,
            requested_amount=requested_amount,
        )
