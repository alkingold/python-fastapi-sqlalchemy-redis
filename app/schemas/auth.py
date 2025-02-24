"""
This module contains schemas for JWT auth token
"""

from pydantic import BaseModel

class Token(BaseModel):
    """
    Schema for JWT response
    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
    Schema for JWT token payload
    """
    username: str

class LoginRequest(BaseModel):
    """
    Schema for user login request
    """
    username: str
    password: str
