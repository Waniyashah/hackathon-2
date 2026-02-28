from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel
from src.database import AsyncSessionLocal, async_engine

# Import all models to ensure they're registered with SQLModel
from src.models.task import Task
from src.models.conversation import Conversation
from src.models.message import Message

@asynccontextmanager
async def get_db_session():
    """
    Async context manager for database sessions.
    Ensures proper session lifecycle management.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def init_db():
    """
    Initialize the database by creating all tables.
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def drop_db():
    """
    Drop all database tables. Use with caution!
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
