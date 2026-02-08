from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.api.auth import router as auth_router
from src.api.tasks import router as tasks_router
from src.models.user import User
from src.models.task import Task
from src.database.session import engine
from src.middleware.security import add_security_headers


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    print("Creating database tables...")
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(bind=engine)
    print("Database tables created.")
    yield
    # Cleanup on shutdown
    print("Shutting down...")


app = FastAPI(
    title="Todo App API",
    description="A simple todo application API with user authentication and task management",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, change this to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add security headers
add_security_headers(app)

# Include routers
app.include_router(auth_router, prefix="/api")
app.include_router(tasks_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to Todo App API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)