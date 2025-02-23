"""
This module contains pydantic schemas for User
"""

from pydantic import BaseModel

class UserBase(BaseModel):
    """
    Pydantic base schema for User
    """
    username: str
    is_admin: bool

class UserCreate(UserBase):
    """
    Pydantic schema user for user creation
    """
    password: str

class UserResponse(UserBase):
    """
    Pydantic schema user response
    """
    id: int

    class Config:
        """
        Pydantic schema config class
        Option to convert SQLAlchemy model
        """
        from_attributes = True
