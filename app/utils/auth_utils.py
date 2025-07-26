from datetime import datetime, timezone, timedelta

import jwt
from passlib.context import CryptContext

from app.config import settings

ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
ALGORITHM = settings.algorithm
SECRET_KEY = settings.secret_key

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    data_to_be_encoded = data.copy()
    token_expiration_time = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_to_be_encoded.update({"exp": token_expiration_time})
    encoded_jwt = jwt.encode(
        data_to_be_encoded, 
        SECRET_KEY, 
        algorithm=ALGORITHM)
    return encoded_jwt