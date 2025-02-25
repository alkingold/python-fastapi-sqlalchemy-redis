"""
This module contains schemas for board actions
"""

from pydantic import BaseModel

class ActionBase(BaseModel):
    """
    Pydantic Base schema for Action
    """
    title: str
    description: str | None = None

class ActionCreate(ActionBase):
    """
    Schema for Action creation
    """

class ActionUpdate(ActionBase):
    """
    Schema for updating an action
    """

class ActionResponse(ActionBase):
    """
    Response schema for an action
    """
    id: int
    user_id: int

    class Config:
        from_attributes = True
