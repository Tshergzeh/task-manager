from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Response, Depends, status, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session, select

from app.database import get_session
from app.models.task import Task
from app.models.user import User
from app.utils.database_utils import save_to_database
from app.utils.task_utils import build_tasks_by_due_date_statement, check_that_task_id_is_valid, check_that_user_owns_task, empty_scalar_tasks_into_list
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
        saved_task = save_to_database(task, session)
        response.status_code = status.HTTP_201_CREATED
        return {
            "success": True, 
            "message": "Task created successfully",
            "data": saved_task
        }
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
    tasks = empty_scalar_tasks_into_list(tasks_scalar_result)    
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
    incomplete_tasks = empty_scalar_tasks_into_list(incomplete_tasks_scaler_result)
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
    completed_tasks = empty_scalar_tasks_into_list(completed_tasks_scaler_result)
    return {"success": True, "completed_tasks": completed_tasks}

@router.get("/api/tasks/by_due_date/", tags=["tasks"])
def get_tasks_by_due_date(
    start_date: datetime | None = None, 
    end_date: datetime | None = None, 
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    if end_date < start_date: # type: ignore
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, 
            "End date greater than start date"
        )
    tasks_by_due_date_scaler_result = session.exec(
        build_tasks_by_due_date_statement(
            current_user, 
            start_date, 
            end_date
        )
    )
    tasks_by_due_date = empty_scalar_tasks_into_list(tasks_by_due_date_scaler_result)
    return {"success": True, "tasks_by_due_date": tasks_by_due_date}

@router.patch("/api/tasks/mark_complete/{task_id}", tags=["tasks"])
def mark_task_as_completed(
    task_id: int, 
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    check_that_task_id_is_valid(task_id, session)
    task = check_that_user_owns_task(current_user.username, task_id, session)
    task.is_completed = True
    save_to_database(task, session)
    return {"success": True, "updated_task": task}

@router.delete("/api/tasks/{task_id}", tags=["tasks"])
def delete_task(
    task_id: int, 
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    check_that_task_id_is_valid(task_id, session)
    task = check_that_user_owns_task(current_user.username, task_id, session)
    session.delete(task)
    session.commit()
    return {"success": True, "deleted_task": task}
