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
) -> Action:
    """
    Retrieve an action by its ID
    """
    result = await db.execute(
        select(Action).where(Action.id == action_id)
    )
    return result.scalars().first()

async def get_user_actions(
    db: AsyncSession,
    user_id: int
) -> list[Action]:
    """
    Retrieve all actions for a given user
    """
    result = await db.execute(select(Action).where(Action.user_id == user_id))
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
