"""
This module contains authentication routes
"""

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.models.user import User
from app.db.crud.user import get_user_by_username
from app.schemas.auth import Token
from app.schemas.user import UserResponse
from app.core.security import verify_password, create_access_token
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=Token)
async def login(
	user_data: OAuth2PasswordRequestForm = Depends(),
	db: AsyncSession = Depends(get_db)
) -> Token:
    """
    Authenticate user and return JWT token
    """
    user: User | None = await get_user_by_username(db, user_data.username)

    if user is None or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=30)
    )

    return Token(access_token=access_token, token_type="bearer")

@router.get("/me", response_model=UserResponse)
async def read_users_me(
    current_user: UserResponse = Depends(get_current_user)
) -> UserResponse:
    """
    Returns current authenticated user
    """
    return UserResponse.model_validate(current_user)
