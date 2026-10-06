from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.database import get_db
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


CurrentUser = Annotated[User, Depends(get_current_user)]
DatabaseSession = Annotated[Session, Depends(get_db)]


def get_owned_task(
    task_id: int,
    current_user: User,
    db: Session,
) -> Task:
    task = db.scalar(
        select(Task).where(
            Task.id == task_id,
            Task.created_by == current_user.id,
        )
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    payload: TaskCreate,
    current_user: CurrentUser,
    db: DatabaseSession,
) -> Task:
    task = Task(
        title=payload.title.strip(),
        description=payload.description,
        status=payload.status.value,
        created_by=current_user.id,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


@router.get(
    "",
    response_model=list[TaskResponse],
)
def get_tasks(
    current_user: CurrentUser,
    db: DatabaseSession,
) -> list[Task]:
    tasks = db.scalars(
        select(Task)
        .where(Task.created_by == current_user.id)
        .order_by(Task.created_at.desc(), Task.id.desc())
    ).all()

    return list(tasks)


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
)
def get_task(
    task_id: int,
    current_user: CurrentUser,
    db: DatabaseSession,
) -> Task:
    return get_owned_task(
        task_id=task_id,
        current_user=current_user,
        db=db,
    )


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
)
def update_task(
    task_id: int,
    payload: TaskUpdate,
    current_user: CurrentUser,
    db: DatabaseSession,
) -> Task:
    task = get_owned_task(
        task_id=task_id,
        current_user=current_user,
        db=db,
    )

    update_data = payload.model_dump(
        exclude_unset=True,
    )

    if "title" in update_data and update_data["title"] is not None:
        task.title = update_data["title"].strip()

    if "description" in update_data:
        task.description = update_data["description"]

    if "status" in update_data and update_data["status"] is not None:
        task.status = update_data["status"].value

    db.commit()
    db.refresh(task)

    return task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task(
    task_id: int,
    current_user: CurrentUser,
    db: DatabaseSession,
) -> None:
    task = get_owned_task(
        task_id=task_id,
        current_user=current_user,
        db=db,
    )

    db.delete(task)
    db.commit()
