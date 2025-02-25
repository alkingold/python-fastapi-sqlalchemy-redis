"""
This module is an entry point of the Action Board FastAPI
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.database import engine, Base
from app.routes.user import router as user_router
from app.routes.auth import router as auth_router
from app.routes.action import router as action_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handle application lifecycles
    """
    print("Starting Action Board application...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield # here cleanup when stopping application
    print("Stopping application...")

app = FastAPI(title="Action Board API", lifespan=lifespan)

app.include_router(user_router, prefix="/api", tags=["Users"])
app.include_router(auth_router)
app.include_router(action_router)
