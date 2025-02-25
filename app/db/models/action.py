"""
This module contains Action database models
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Action(Base):
    """
    SQLAlchemy model for actions on the board
    """
    __tablename__ = "actions"

    id = Column(Integer, primary_key=True, index=True)
    title =  Column(String, nullable=False)
    description = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="actions")

    def __repr__(self):
        return f"<Action(id={self.id}, title={self.title}, description={self.description}, user_id={self.user_id})>"
