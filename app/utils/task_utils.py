from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.models.task import Task

def checkThatUserOwnsTask(username: str, task_id: int, session: Session):
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
