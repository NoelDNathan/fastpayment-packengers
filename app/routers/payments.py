from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from uuid import UUID

from app.models.payments import Payment
from app.schemas.payments import PaymentCreate, PaymentResponse, PaymentStatusUpdate
from app.database import get_db

router = APIRouter(prefix="/payments", tags=["Payments"])


# Create a new payment
@router.post("/", response_model=PaymentResponse)
async def create_payment(payment: PaymentCreate, db: AsyncSession = Depends(get_db)):
    new_payment = Payment(
        advance_request_id=payment.advance_request_id,
        paid_amount=payment.paid_amount,
        payment_method=payment.payment_method,
        payment_date=payment.payment_date,
        bank_reference=payment.bank_reference,
        payment_status=payment.status,
    )

    db.add(new_payment)
    await db.commit()
    await db.refresh(new_payment)
    return new_payment


# Get one payment by its ID
@router.get("/{payment_id}", response_model=PaymentResponse)
async def get_payment(payment_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Payment).filter(Payment.payment_id == payment_id))
    payment = result.scalars().one_or_none()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


# Get all payments, optionally filtered by advance_request_id
@router.get("/", response_model=List[PaymentResponse])
async def get_all_payments(
    advance_request_id: Optional[int] = None, db: AsyncSession = Depends(get_db)
):
    stmt = select(Payment)
    if advance_request_id is not None:
        stmt = stmt.filter(Payment.advance_request_id == advance_request_id)
    result = await db.execute(stmt)
    return result.scalars().all()


# Update the status of a payment
@router.patch("/{payment_id}/status", response_model=PaymentResponse)
async def update_payment_status(
    payment_id: UUID,
    status_update: PaymentStatusUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Payment).filter(Payment.payment_id == payment_id))
    payment = result.scalars().one_or_none()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    payment.payment_status = status_update.status
    await db.commit()
    await db.refresh(payment)
    return payment
