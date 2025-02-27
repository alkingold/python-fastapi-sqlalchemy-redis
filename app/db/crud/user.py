"""
This module contains database CRUD operations for users
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password

async def create_user(
	db: AsyncSession,
	user_data: UserCreate
) -> User:
    """
    Creates new user in the database

    Args:
        db (AsyncSession): Async database session
        user_data: UserCreate

    Returns:
        User: SQLAlchemy ORM User object instance
    """
    hashed_pw = hash_password(user_data.password)
    new_user = User(
        username=user_data.username,
        hashed_password=hashed_pw,
        is_admin=user_data.is_admin
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    """
    Gets user by username from database
    Returns None if user not found
    """
    stmt = select(User).where(User.username == username)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def get_users(db: AsyncSession):
    """
    Gets all users
    """
    result = await db.execute(select(User))
    return result.scalars().all()
