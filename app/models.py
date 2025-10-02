from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict

class UserBase(BaseModel):
    """Базовый класс с общими полями для всех пользовательских моделей"""
    name: str
    email: EmailStr

class UserCreate(UserBase):
    pass 

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class HealthCheckResponse(BaseModel):
    status: str
    database: str
    timestamp: datetime
    environment: str
    
class StatsResponse(BaseModel):
    total_users: int
    avg_name_length: float
    first_user_date: datetime
    last_user_date: datetime