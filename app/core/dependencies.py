"""
This module contains authentication dependencies
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_access_token
from app.db.database import get_db
from app.db.models.user import User
from app.db.models.action import Action
from app.db.crud.user import get_user_by_username
from app.db.crud.action import get_action
from app.schemas.auth import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Retrieve current authenticated user from token
    """
    try:
        payload = decode_access_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise ValueError("Invalid token payload")
        token_data = TokenData(username=username)
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        ) from err

    user = await get_user_by_username(db, username=token_data.username)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user

async def get_current_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Retrieve current admin user or throw an exception

    Args:
        current_user (User): Currently authenticated user

    Returns:
        User: Currently authenticated admin user

    Raises:
        HTTPException: Raises 403 HTTP error when not admin user
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return current_user

async def get_current_user_authorised_by_action(
    action_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Ensures that user is either admin or owner of the action
    Returns the action if operation on the action can be performed

    Args:
        action_id (int): ID of the action to manage
        current_user (User): currently connected user
        db (AsyncSession): Database async session

    Returns:
        User: Returns connected user authorised to manage action

    Raises:
        HTTPException:
            - 404 if action does not exist
            - 403 if user is not authorised to edit action
    """
    action: Action = await get_action(db, action_id)
    if not action:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )

    if action.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorised to modify this action"
        )

    return current_user
