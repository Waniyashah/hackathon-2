from sqlmodel import create_engine, Session
import os
from typing import Generator

# Database URL - using Neon PostgreSQL
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://username:password@localhost:5432/todo_app"
)

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session