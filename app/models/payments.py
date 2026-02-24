from sqlalchemy import Column, Integer, Numeric, String, DateTime
from sqlalchemy.sql import func
from database import Base
from sqlalchemy import Enum as SAEnum
from enum import Enum

class PaymentStatus(str, Enum): 
    PENDING = "pending"
    PAID = "paid"

PaymentStatusEnum = SAEnum(PaymentStatus, name="payment_status")

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    advance_request_id = Column(Integer, nullable=True)
    paid_amount = Column(Numeric(10, 2), nullable=False)
    payment_method = Column(String, nullable=False)
    payment_date = Column(DateTime(timezone=True), nullable=False)
    bank_reference = Column(String, nullable=False)
    status = Column(PaymentStatusEnum, nullable=False, default=PaymentStatus.PENDING)

