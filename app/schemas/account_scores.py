from pydantic import BaseModel, constr
from datetime import datetime
from uuid import UUID

class AccountScoreCreate(BaseModel):
    account_id: UUID

class AccountScoreUpdate(BaseModel):
    total_requests: int
    approved_requests: int
    rejected_requests: int
    risk_level: constr(min_length=1, max_length=20)

class AccountScoreResponse(BaseModel):
    account_score_id: UUID
    account_id: UUID
    total_requests: int
    approved_requests: int
    rejected_requests: int
    risk_level: str
    updated_at: datetime

    class Config:
        orm_mode = True
