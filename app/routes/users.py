from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import exc
from sqlmodel import Session

from app.database import get_session
from app.models.user import UserLogin
from app.utils.user_utils import build_user_model
from app.utils.database_utils import save_to_database

router = APIRouter()

@router.post("/api/users", tags=["users"])
def create_user(
    new_user: UserLogin, 
    response: Response, 
    session: Session = Depends(get_session)
):
    try:
        user_model = build_user_model(new_user)
        save_to_database(user_model, session)
        session.refresh(user_model)
    except exc.IntegrityError as e:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            f"User {new_user.username} already exists"
        )
    except Exception as ex:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            f"User creation failed with error: {ex}"
        )
    
    response.status_code = status.HTTP_201_CREATED
    return {"success": True, "message": "User created successfully"}
