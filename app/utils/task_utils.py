from datetime import datetime

from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.models.task import Task
from app.models.user import User

def empty_scalar_tasks_into_list(scalar_result):
    tasks = []

    for task_result in scalar_result:
        task = task_result.model_dump()
        tasks.append(task)

    return tasks

def check_that_task_id_is_valid(task_id: int, session: Session):
    valid_task = session.get(Task, task_id)
    if not valid_task:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Invalid task ID")

def check_that_user_owns_task(username: str, task_id: int, session: Session):
    task = session.exec(
        select(Task)
            .where(Task.owner == username)
            .where(Task.id == task_id)
    )

    if not task:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, 
            "Task does not belong to user"
        )
    
    return task.one()

def build_tasks_by_due_date_statement(
    current_user: User,
    start_date: datetime | None = None, 
    end_date: datetime | None = None
):
    if start_date and not end_date:
        return select(Task).where(Task.owner == current_user.username).where(Task.due_date >= start_date) # type: ignore
    if not start_date and end_date:
        return select(Task).where(Task.owner == current_user.username).where(Task.due_date <= end_date) # type: ignore
    if start_date and end_date:
        return select(Task).where(Task.owner == current_user.username).where(Task.due_date >= start_date).where(Task.due_date <= end_date) # type: ignore
    return select(Task).where(Task.owner == current_user.username)