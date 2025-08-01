from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

from models import UserDB
from database import users_collection
from config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

async def authenticate_user(username: str, password: str):
    user_data = await users_collection.find_one({"username": username})
    if not user_data or not verify_password(password, user_data["hashed_password"]):
        return False
    
    try:
        # Преобразуем ObjectId в строку для корректной валидации
        user_data["_id"] = str(user_data["_id"])
        user = UserDB.model_validate(user_data)  # Используем model_validate вместо **
        return user
    except Exception as e:
        print(f"Error creating UserDB: {e}")
        return False

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt