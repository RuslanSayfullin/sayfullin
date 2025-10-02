from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr, ConfigDict

class UserBase(BaseModel):
    name: str
    email: EmailStr
    bio: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    bio: Optional[str] = None

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    author_id: int

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class Post(PostBase):
    id: int
    author_id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class PostWithUser(Post):
    author: Optional[User] = None

class UserWithPosts(User):
    posts: List[Post] = []

class HealthCheckResponse(BaseModel):
    status: str
    database: str
    timestamp: datetime
    environment: str

class StatsResponse(BaseModel):
    total_users: int
    total_posts: int
    avg_name_length: float
    first_user_date: datetime
    last_user_date: datetime