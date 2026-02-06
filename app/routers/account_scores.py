from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from models.account_scores import AccountScore
from schemas.account_scores import (
    AccountScoreCreate,
    AccountScoreUpdate,
    AccountScoreResponse
)
from database import get_db

router = APIRouter(
    prefix="/account-scores",
    tags=["Account Scores"]
)

# Create score record (usually internal)
@router.post("/", response_model=AccountScoreResponse)
def create_account_score(
    score: AccountScoreCreate,
    db: Session = Depends(get_db)
):
    existing = (
        db.query(AccountScore)
        .filter(AccountScore.account_id == score.account_id)
        .first()
    )

    if existing:
        raise HTTPException(status_code=400, detail="Account score already exists")

    new_score = AccountScore(
        account_id=score.account_id,
        risk_level="low"
    )

    db.add(new_score)
    db.commit()
    db.refresh(new_score)
    return new_score


# Get score by account_id
@router.get("/{account_id}", response_model=AccountScoreResponse)
def get_account_score(account_id: UUID, db: Session = Depends(get_db)):
    score = (
        db.query(AccountScore)
        .filter(AccountScore.account_id == account_id)
        .first()
    )

    if not score:
        raise HTTPException(status_code=404, detail="Account score not found")

    return score


# Update account score (system-driven)
@router.patch("/{account_id}", response_model=AccountScoreResponse)
def update_account_score(
    account_id: UUID,
    update: AccountScoreUpdate,
    db: Session = Depends(get_db)
):
    score = (
        db.query(AccountScore)
        .filter(AccountScore.account_id == account_id)
        .first()
    )

    if not score:
        raise HTTPException(status_code=404, detail="Account score not found")

    score.total_requests = update.total_requests
    score.approved_requests = update.approved_requests
    score.rejected_requests = update.rejected_requests
    score.risk_level = update.risk_level

    db.commit()
    db.refresh(score)
    return score
