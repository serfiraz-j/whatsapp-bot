from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings
from app.models.base import Base
from app.models.user import User

# Create the async engine
engine = create_async_engine(settings.DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_db_and_tables():
    """
    Initializes the database and creates tables if they don't exist.
    This is called on application startup.
    """
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all) # Use for development to reset DB
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get an async database session.
    """
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """
    Dependency to get the user database adapter for FastAPI Users.
    """
    yield SQLAlchemyUserDatabase(session, User)
