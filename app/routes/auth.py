from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.database import get_session
from app.models.user import UserLogin, User
from app.utils.auth_utils import verify_password, create_access_token

router = APIRouter()

@router.post("/api/auth/login", tags=["auth"])
def login_user(
    login_form: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    user = session.get(User, login_form.username)

    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,"Invalid credentials")
    
    if not verify_password(login_form.password, user.hashed_password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Incorrect password")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"success": True, "access_token": access_token}
