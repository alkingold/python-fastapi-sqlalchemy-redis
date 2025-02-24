"""
This module contains user related routes
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserResponse
from app.db.crud.user import create_user, get_user_by_username, get_users
from app.db.database import get_db
from app.core.dependencies import get_current_user

router = APIRouter()

@router.post("/users", response_model=UserResponse)
async def add_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)) -> UserResponse:
    """
    Route that handles creation if a new user

    Args:
        user_data (UserCreate): Inscription user data
        db (AsyncSession): Async database session

    Returns:
        UserResponse: Created user without password

    Raises:
        HTTPException: If username is not unique
    """
    try:
        existing_user = await get_user_by_username(db, user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This username is already taken"
            )

        user = await create_user(db, user_data)
        return UserResponse.model_validate(user)
    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        ) from exc

@router.get("/users")
async def list_users(db: AsyncSession = Depends(get_db)):
    """
    Route that gets all users list

    Args:
        db (AsyncSession): Async database session

    Returns:
    """
    return await get_users(db)

@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: UserResponse = Depends(get_current_user)
) -> UserResponse:
    """
    Retrieve current user profile
    """
    return UserResponse.model_validate(current_user)
