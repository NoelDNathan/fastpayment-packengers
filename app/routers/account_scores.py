from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.models.account_scores import AccountScore
from app.schemas.account_scores import (
    AccountScoreCreate,
    AccountScoreUpdate,
    AccountScoreResponse
)
from app.database import get_db

router = APIRouter(
    prefix="/account-scores",
    tags=["Account Scores"]
)

# Create score record (usually internal)
@router.post("/", response_model=AccountScoreResponse)
async def create_account_score(
    score: AccountScoreCreate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(AccountScore).filter(AccountScore.account_id == score.account_id)
    )
    existing = result.scalars().one_or_none()

    if existing:
        raise HTTPException(status_code=400, detail="Account score already exists")

    new_score = AccountScore(
        account_id=score.account_id,
        risk_level="low"
    )

    db.add(new_score)
    await db.commit()
    await db.refresh(new_score)
    return new_score


# Get score by account_id
@router.get("/{account_id}", response_model=AccountScoreResponse)
async def get_account_score(account_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(AccountScore).filter(AccountScore.account_id == account_id)
    )
    score = result.scalars().one_or_none()

    if not score:
        raise HTTPException(status_code=404, detail="Account score not found")

    return score


# Update account score (system-driven)
@router.patch("/{account_id}", response_model=AccountScoreResponse)
async def update_account_score(
    account_id: UUID,
    update: AccountScoreUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(AccountScore).filter(AccountScore.account_id == account_id)
    )
    score = result.scalars().one_or_none()

    if not score:
        raise HTTPException(status_code=404, detail="Account score not found")

    score.total_requests = update.total_requests
    score.approved_requests = update.approved_requests
    score.rejected_requests = update.rejected_requests
    score.risk_level = update.risk_level

    await db.commit()
    await db.refresh(score)
    return score
