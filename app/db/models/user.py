"""
This module contains User database models
"""

from sqlalchemy import Column, Integer, String, Boolean
from app.db.database import Base

class User(Base):
    """
    Represents a User SQLAlchemy model

    This class is a model SQLAlchemy for 'users' table
    It contains informations related to a user

    Attributes:
        id (int): Primary key, automatically generated, unique user identifier.
        username (str): User's unique username.
        hashed_password (str): User's hashed password.
        is_admin (bool): Whether user is admin default to False)
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"
