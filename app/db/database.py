"""
This module handles SQLAlchemy database connexion configuration
"""

from typing import AsyncGenerator
import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base, DeclarativeMeta
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, future=True, echo=True)

async_session_maker = sessionmaker(
	bind=engine,
	class_=AsyncSession,
	expire_on_commit=False
)

Base: DeclarativeMeta = declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
