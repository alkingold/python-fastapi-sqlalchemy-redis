"""
This module contains board actions related routes
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.db.crud.action import create_action, get_action, \
    get_user_actions, update_action, delete_action
from app.schemas.action import ActionCreate, ActionUpdate, ActionResponse
from app.core.dependencies import get_current_user
from app.db.models.user import User

router = APIRouter(prefix="/actions", tags=["Actions"])

@router.post("/", response_model=ActionResponse, status_code=status.HTTP_201_CREATED)
async def create_new_action(
	action_data: ActionCreate,
	db: AsyncSession = Depends(get_db),
	current_user: User = Depends(get_current_user)
):
    """
    Create a new action for the authenticated user
    """
    return await create_action(db, user_id=current_user.id, action_data=action_data)

@router.get("/{action_id}", response_model=ActionResponse)
async def read_action(
    action_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve a specific action
    """
    action = await get_action(db, action_id)
    if action is None or action.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Action not found"
        )
    return action

@router.get("/", response_model=list[ActionResponse])
async def read_user_actions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> list[ActionResponse]:
    """
    Retrieve all actions of the authenticated used
    """
    return await get_user_actions(db, current_user.id)

@router.put("/{action_id}", response_model=ActionResponse)
async def update_existing_action(
    action_id: int,
    action_data: ActionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ActionResponse:
    """
    Update an existing action
    """
    action = await get_action(db, action_id)
    if action is None or action.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    updated_action = await update_action(db, action_id, action_data)
    return updated_action

@router.delete("/{action_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_action(
    action_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete an action
    """
    action = await get_action(db, action_id)
    if action is None or action.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Action not found"
        )

    await delete_action(db, action_id)
