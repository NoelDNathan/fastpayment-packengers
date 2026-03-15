"""Auth router."""

from __future__ import annotations
from fastapi import APIRouter, HTTPException, status, Depends     
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import accounts as account_models
from app.schemas.accounts import AccountCreate
from app.database import get_async_db
from app.utils.hashing import PasswordSecurity
from app.utils.third_party_auth import ThirdPartyAuth

auth_router = APIRouter(prefix="/user-authentication", tags=["User Authentication"])

third_party_auth = ThirdPartyAuth()
auth_router.post("/login/google")(third_party_auth.google_login)
auth_router.get("/login/facebook")(third_party_auth.facebook_login)
auth_router.get("/auth/facebook/callback")(third_party_auth.facebook_callback)


# --- Registration ---
@auth_router.post("/register")
async def create_user(account: AccountCreate, db: AsyncSession = Depends(get_async_db)):
    # Check if email exists
    result = await db.execute(
        select(account_models.Accounts).where(account_models.Accounts.email == account.email)
    )
    user = result.scalar_one_or_none()
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    # Hash password & save new user
    hashed_pw = PasswordSecurity.hash(account.password)
    created_user = account_models.Accounts(email=account.email, hashed_password=hashed_pw)
    db.add(created_user)
    await db.commit()
    await db.refresh(created_user)

    return {"message": "User registered successfully", "email": created_user.email}


# --- Login ---
@auth_router.post("/login")
async def login_user(account: AccountCreate, db: AsyncSession = Depends(get_async_db)):
    # Get user by email
    result = await db.execute(
        select(account_models.Accounts).where(account_models.Accounts.email == account.email)
    )
    user = result.scalar_one_or_none()

    # Verify credentials
    if not user or not PasswordSecurity.verify(account.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")

    return {"message": "Login successful", "email": user.email}



   