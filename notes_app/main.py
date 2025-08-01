
from typing import Annotated
from datetime import datetime, timedelta, timezone


from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm

from models import (
    UserCreate, UserOut, Token
)
from auth import (
    get_password_hash, create_access_token
)
from database import users_collection
from auth import authenticate_user
from config import settings

app = FastAPI(title="Notes API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # Разрешает запросы с ЛЮБОГО домена
    allow_credentials=True, # Разрешает отправку кук и авторизационных заголовков
    allow_methods=["*"],    # Разрешает ВСЕ HTTP-методы (GET, POST и т.д.)
    allow_headers=["*"],    # Разрешает ВСЕ заголовки в запросах
)

# Регистрация
@app.post("/auth/register", response_model=UserOut)
async def register(user: UserCreate):

    if await users_collection.find_one({"username": user.username}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    if await users_collection.find_one({"email": user.email}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_password = get_password_hash(user.password)
    user_dict = user.model_dump(exclude={"password"})
    user_dict.update({
        "hashed_password": hashed_password,
        "created_at": datetime.now(timezone.utc)
    })

    result = await users_collection.insert_one(user_dict)
    created_user = await users_collection.find_one({"_id": result.inserted_id})
    print(created_user, "123")
    return UserOut(**created_user, id=str(result.inserted_id))

# Аутентификация
@app.post("/auth/login", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    print(form_data.username, form_data.password)
    user = await authenticate_user(form_data.username, form_data.password)
   
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
