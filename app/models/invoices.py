from sqlalchemy import Column, Integer, Numeric, String, DateTime
from sqlalchemy.sql import func
from database import Base

import uuid
from sqlalchemy import Column, Numeric, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from database import Base

class InvoiceStatus(str, Enum): 
    PENDING = "pending"
    PAID = "paid"
    OVERDUE = "overdue"
   
class Payment(Base):
    __tablename__ = "payments"

    payment_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    account_id = Column(UUID(as_uuid=True), nullable=False)  # matches accounts table
    advance_request_id = Column(UUID(as_uuid=True), nullable=True)  # optional link
    paid_amount = Column(Numeric(10, 2), nullable=False)
    payment_method = Column(String, nullable=False)
    payment_date = Column(DateTime(timezone=True), nullable=False)
    bank_reference = Column(String, nullable=False)
    status = Column(String, nullable=False, default="pending")  # pending, completed, failed
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)




InvoiceStatusEnum = SAEnum(InvoiceStatus, name="invoice_status")