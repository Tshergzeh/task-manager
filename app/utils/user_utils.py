from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt.exceptions import InvalidTokenError
from sqlmodel import Session

from app.config import settings
from app.database import get_session
from app.models.user import User, UserLogin
from app.utils.auth_utils import generate_password_hash

ALGORITHM = settings.algorithm
SECRET_KEY = settings.secret_key

security = HTTPBearer()

def build_user_model(user: UserLogin) -> User:
    user_dict = user.model_dump()
    user_dict["hashed_password"] = generate_password_hash(user.password)
    return User(**user_dict)

async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        session: Session = Depends(get_session)
):
    token = credentials.credentials

    credentials_exception = HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        "Could not validate credentials",
        {"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        user = session.get(User, username)
        return user
    except InvalidTokenError:
        raise credentials_exception
    