import pyotp
import qrcode
import io
import os
from fastapi import APIRouter, HTTPException, Body, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.accounts import Account
from google.oauth2 import id_token  
from google.auth.transport import requests as google_requests
from app.database import get_db

# Router for FastAPI
third_party_router = APIRouter()

# Get GOOGLE_CLIENT_ID from environment
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")


                 #QR / 2FA 
async def generate_qr(username: str, db: AsyncSession) -> bytes:
    # Get user's OTP secret
    result = await db.execute(select(Account).where(Account.email == username))
    user = result.scalar_one_or_none()
    if not user or not user.otp_secret:
        raise HTTPException(status_code=404, detail="User not found")

    # Generate TOTP QR code
    uri = pyotp.totp.TOTP(user.otp_secret).provisioning_uri(name=username, issuer_name="SecureApp")
    img = qrcode.make(uri)
    buf = io.BytesIO()
    img.save(buf)
    buf.seek(0)
    return buf.getvalue()

# --- GOOGLE LOGIN ---
async def login_google(token: str, db: AsyncSession) -> str:
    try:
        idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), GOOGLE_CLIENT_ID)
        email = idinfo["email"]

        result = await db.execute(select(Account).where(Account.email == email))
        user = result.scalar_one_or_none()

        if not user:
            # Create user in DB (hashed_password can be placeholder for OAuth)
            new_user = Account(email=email, hashed_password="OAUTH_GOOGLE", otp_secret=None)
            db.add(new_user)
            await db.commit()
            await db.refresh(new_user)
        return email
    except Exception:
        raise HTTPException(status_code=400, detail="Google Auth Failed")


# --- FACEBOOK LOGIN ---
async def login_facebook(fb_token: str, db: AsyncSession) -> str:
    # Here you can use `httpx.AsyncClient` to get user info from FB Graph API
    # Example:
    # async with httpx.AsyncClient() as client:
    #     user_res = await client.get("https://graph.facebook.com/me", params={...})
    #     fb_user = user_res.json()
    #     email = fb_user.get("email") or fb_user.get("id")
    #     ...
    #     return email
    pass  # implement async HTTP call

# Add FastAPI route wrappers

@third_party_router.post("/login/google")
async def google_login_endpoint(
    token: str = Body(...), db: AsyncSession = Depends(get_db)
):
    """
    Endpoint to log in a user via Google OAuth2 token.
    """
    email = await login_google(token, db)
    return JSONResponse({"email": email})


@third_party_router.post("/login/facebook")
async def facebook_login_endpoint(
    fb_token: str = Body(...), db: AsyncSession = Depends(get_db)
):
    """
    Endpoint to log in a user via Facebook token.
    """
    email = await login_facebook(fb_token, db)
    return JSONResponse({"email": email})