from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from models.payments import Payment
from schemas.payments import PaymentCreate, PaymentResponse, PaymentStatusUpdate
from database import get_db

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)

# Create a new payment
@router.post("/", response_model=PaymentResponse)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    new_payment = Payment(
        advance_request_id=payment.advance_request_id,
        paid_amount=payment.paid_amount,
        payment_method=payment.payment_method,
        payment_date=payment.payment_date,
        bank_reference=payment.bank_reference,
        status=payment.status
    )

    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment


# Get one payment by its ID
@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


# Get all payments, optionally filtered by advance_request_id
@router.get("/", response_model=List[PaymentResponse])
def get_all_payments(advance_request_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(Payment)
    if advance_request_id is not None:
        query = query.filter(Payment.advance_request_id == advance_request_id)
    return query.all()


# Update the status of a payment
@router.patch("/{payment_id}/status", response_model=PaymentResponse)
def update_payment_status(payment_id: int, status_update: PaymentStatusUpdate, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    payment.status = status_update.status
    db.commit()
    db.refresh(payment)
    return payment
