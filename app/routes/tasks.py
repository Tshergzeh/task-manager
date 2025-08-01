from typing import Annotated

from fastapi import APIRouter, Response, Depends, status, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session, select

from app.database import get_session
from app.models.task import Task
from app.models.user import User
from app.utils.database_utils import save_to_database
from app.utils.task_utils import checkThatTaskIdIsValid, checkThatUserOwnsTask, emptyScalarTasksIntoList
from app.utils.user_utils import get_current_user

router = APIRouter()

@router.post("/api/tasks", tags=["tasks"])
async def create_task(
    task: Task, 
    response: Response,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    try:
        save_to_database(task, session)
        response.status_code = status.HTTP_201_CREATED
        return {"success": True, "message": "Task created successfully"}
    except Exception as ex:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            f"Task creation failed with error: {ex}"
        )
    
@router.get("/api/tasks", tags=["tasks"])
def get_all_tasks_for_user(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    username = current_user.username
    tasks_scalar_result = session.exec(
        select(Task).where(Task.owner == username)
    )
    tasks = emptyScalarTasksIntoList(tasks_scalar_result)    
    return {"success": True, "tasks": tasks}

@router.get("/api/tasks/incomplete", tags=["tasks"])
def get_incomplete_tasks_for_user(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    incomplete_tasks_scaler_result = session.exec(
        select(Task)
            .where(Task.owner == current_user.username)
            .where(Task.is_completed == False)
    )
    incomplete_tasks = emptyScalarTasksIntoList(incomplete_tasks_scaler_result)
    return {"success": True, "incomplete_tasks": incomplete_tasks}

@router.get("/api/tasks/completed", tags=["tasks"])
def get_completed_tasks_for_user(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    completed_tasks_scaler_result = session.exec(
        select(Task)
            .where(Task.owner == current_user.username)
            .where(Task.is_completed == True)
    )
    completed_tasks = emptyScalarTasksIntoList(completed_tasks_scaler_result)
    return {"success": True, "completed_tasks": completed_tasks}

@router.patch("/api/tasks/mark_complete/{task_id}", tags=["tasks"])
def mark_task_as_completed(
    task_id: int, 
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    checkThatTaskIdIsValid(task_id, session)
    task = checkThatUserOwnsTask(current_user.username, task_id, session)
    task.is_completed = True
    save_to_database(task, session)
    return {"success": True, "updated_task": task}

@router.delete("/api/tasks/{task_id}", tags=["tasks"])
def delete_task(
    task_id: int, 
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    checkThatTaskIdIsValid(task_id, session)
    task = checkThatUserOwnsTask(current_user.username, task_id, session)
    session.delete(task)
    session.commit()
    return {"success": True, "deleted_task": task}
