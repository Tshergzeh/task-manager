from app.models.user import User, UserLogin
from app.utils.auth_utils import generate_password_hash

def build_user_model(user: UserLogin) -> User:
    user_dict = user.model_dump()
    user_dict["hashed_password"] = generate_password_hash(user.password)
    return User(**user_dict)