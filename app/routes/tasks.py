from fastapi import APIRouter, Response, Depends, status, HTTPException
from sqlmodel import Session

from app.database import get_session
from app.models.task import Task
from app.utils.database_utils import save_to_database

router = APIRouter()

@router.post("/api/tasks", tags=["tasks"])
def create_task(
    task: Task, 
    response: Response, 
    session: Session = Depends(get_session)
):
    try:
        save_to_database(task, session)
        session.refresh(task)
        response.status_code = status.HTTP_201_CREATED
        return {"success": True, "message": "Task created successfully"}
    except Exception as ex:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            f"Task creation failed with error: {ex}"
        )
    