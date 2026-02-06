from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import DateTime
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from datetime import datetime

from models.advance_requests import AdvanceRequest
from schemas.advance_requests import (
    AdvanceRequestCreate,
    AdvanceRequestResponse,
    AdvanceRequestReview
)
from database import get_db

router = APIRouter(
    prefix="/advance-requests",
    tags=["Advance Requests"]
)

# Create advance request
@router.post("/", response_model=AdvanceRequestResponse)
def create_advance_request(
    request: AdvanceRequestCreate,
    db: Session = Depends(get_db)
):
    new_request = AdvanceRequest(
        invoice_id=request.invoice_id,
        requested_amount=request.requested_amount
    )

    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return new_request


# Get one advance request
@router.get("/{advance_request_id}", response_model=AdvanceRequestResponse)
def get_advance_request(advance_request_id: UUID, db: Session = Depends(get_db)):
    request = (
        db.query(AdvanceRequest)
        .filter(AdvanceRequest.advance_request_id == advance_request_id)
        .first()
    )

    if not request:
        raise HTTPException(status_code=404, detail="Advance request not found")

    return request


# Review (approve / reject)
@router.patch("/{advance_request_id}/review", response_model=AdvanceRequestResponse)
def review_advance_request(
    advance_request_id: UUID,
    review: AdvanceRequestReview,
    db: Session = Depends(get_db)
):
    request = (
        db.query(AdvanceRequest)
        .filter(AdvanceRequest.advance_request_id == advance_request_id)
        .first()
    )

    if not request:
        raise HTTPException(status_code=404, detail="Advance request not found")

    request.status = review.status.value
    request.review_comment = review.review_comment
    request.reviewed_at = DateTime

    db.commit()
    db.refresh(request)
    return request
