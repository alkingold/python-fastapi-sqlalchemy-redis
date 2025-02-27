"""
This module contains board actions related routes
"""

from fastapi import APIRouter, Depends, HTTPException, \
    status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.db.crud.action import create_action, get_action, \
    get_actions, update_action, delete_action
from app.schemas.action import ActionCreate, ActionUpdate, ActionResponse
from app.core.dependencies import get_current_user, \
    get_current_user_authorised_by_action
from app.db.models.user import User

router = APIRouter(prefix="/actions", tags=["Actions"])

@router.post("/", response_model=ActionResponse, status_code=status.HTTP_201_CREATED)
async def create_new_action(
	action_data: ActionCreate,
	db: AsyncSession = Depends(get_db),
	current_user: User = Depends(get_current_user)
):
    """
    Create a new board action
    Any authenticated user can create an action
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
    - Regular user can only access its own actions
    - Admin user can access all actions
    """
    action = await get_action(db, action_id)
    if action is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Action not found"
        )

    if not current_user.is_admin and action.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorised to access this action"
        )

    return action

@router.get("/", response_model=list[ActionResponse])
async def read_actions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    page: int = Query(1, ge=1), # Default to first page
    page_size: int = Query(10, ge=1, le=100) # Max 100 items
) -> list[ActionResponse]:
    """
    Retrieve a paginated list of actions
    - Admins get all actions
    - Regular users only get their own actions
    - Uses `page` and `page_size` for pagination
    """
    return await get_actions(
        db=db,
        user_id=current_user.id,
        is_admin=current_user.is_admin,
        page=page,
        page_size=page_size
    )

@router.put("/{action_id}", response_model=ActionResponse)
async def update_existing_action(
    action_id: int,
    action_data: ActionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_authorised_by_action)
) -> ActionResponse:
    """
    Update an existing action:
    - Users can update their own actions
    - Admins can update any action
    """
    updated_action = await update_action(db, action_id, action_data)
    return updated_action

@router.delete("/{action_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_action(
    action_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_authorised_by_action)
):
    """
    Delete an action:
    - Users can delete their own actions
    - Admins can delete any action
    """

    await delete_action(db, action_id)
