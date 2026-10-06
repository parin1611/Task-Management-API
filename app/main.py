from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.tasks import router as tasks_router
from app.db.database import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(
    title="Task Management API",
    description="A small production-style task management REST API.",
    version="1.0.0",
    lifespan=lifespan,
)


app.include_router(auth_router)
app.include_router(tasks_router)


@app.get(
    "/health",
    tags=["Health"],
)
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "task-management-api",
    }
