import os
from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://neondb_owner:npg_abhSCMsW0qc5@ep-dry-hall-ai9qar32-pooler.c-4.us-east-1.aws.neon.tech/neondb")

# Use psycopg_async for async operations
async_engine = create_async_engine(
    DATABASE_URL.replace("postgresql+psycopg://", "postgresql+psycopg_async://"),
    echo=True,  # Log SQL statements
    future=True
)

AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

