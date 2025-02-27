"""
This module contains database CRUD operations for board actions
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.action import Action
from app.schemas.action import ActionCreate, ActionUpdate

async def create_action(
    db: AsyncSession,
    user_id: int,
    action_data: ActionCreate
) -> Action:
    """
    Create a new action in the database
    """
    action = Action(**action_data.model_dump(), user_id=user_id)
    db.add(action)
    await db.commit()
    await db.refresh(action)
    return action

async def get_action(
    db: AsyncSession,
    action_id: int
) -> Action | None:
    """
    Retrieve an action by its ID
    """
    result = await db.execute(
        select(Action).where(Action.id == action_id)
    )
    return result.scalar_one_or_none()

async def get_actions(
    db: AsyncSession,
    user_id: int,
    is_admin: bool,
    page: int = 1,
    page_size: int = 10
) -> list[Action]:
    """
    Retrieve all actions based on user role
    - Admins get all actions
    - Regular users get only their own actions
    - Pagination is applied using `limit` and `offset`
    - Limit and offset are calculated from page number and items per page params

    Args:
        db (AsyncSession): Database async session
        user_id (int): ID of the currently connected user
        is_admin (bool): Whether current user has admin role
        page (int): Page number
        page_size (int): number of items per page

    Returns:
        list[Action]: List of actions based on user role
        - All actions for admins
        - User's actions for regular user
    """
    offset = (page - 1) * page_size

    query = select(Action)

    if not is_admin:
        query = query.where(Action.user_id == user_id)

    query = query.limit(page_size).offset(offset)

    result = await db.execute(query)
    return result.scalars().all()

async def update_action(
    db: AsyncSession,
    action_id: int,
    action_data: ActionUpdate
) -> Action | None:
    """
    Update an existing action
    """
    action = await get_action(db, action_id)
    if action:
        for key, value in action_data.model_dump(exclude_unset=True).items():
            setattr(action, key, value)
        await db.commit()
        await db.refresh(action)
    return action

async def delete_action(db: AsyncSession, action_id: int) -> bool:
    """
    Delete an action from the database
    """
    action = await get_action(db, action_id)
    if action:
        await db.delete(action)
        await db.commit()
        return True
    return False
