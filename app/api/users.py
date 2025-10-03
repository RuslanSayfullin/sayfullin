from typing import List, Optional

from fastapi import APIRouter, status, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from app.schemas import User as UserSchema, UserCreate, UserUpdate, UserWithPosts

from app.database import get_db
from app.models import User
from app.dependencies import get_user_by_id, validate_email_unique

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    # Check if email already exists
    result = await db.execute(select(User).where(User.email == user.email))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    db_user = User(**user.model_dump())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

@router.get("/", response_model=List[UserSchema])
async def read_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).order_by(User.created_at.desc()).offset(skip).limit(limit))
    users = result.scalars().all()
    return users

@router.get("/{user_id}", response_model=UserSchema)
async def read_user(user: User = Depends(get_user_by_id)):
    return user

@router.get("/{user_id}/with-posts", response_model=UserWithPosts)
async def read_user_with_posts(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.id == user_id).options(selectinload(User.posts)))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.put("/{user_id}", response_model=UserSchema)
async def update_user(
    user_update: UserUpdate,
    user: User = Depends(get_user_by_id),
    db: AsyncSession = Depends(get_db)
):
    # Check email uniqueness if email is being updated
    if user_update.email and user_update.email != user.email:
        await validate_email_unique(user_update.email, db, user.id)

    update_data = user_update.model_dump(exclude_unset=True)
    if not update_data:
        return user
    
    stmt = (
        update(User)
        .where(User.id == user.id)
        .values(**update_data)
        .execution_options(synchronize_session="fetch")
    )
    await db.execute(stmt)
    await db.commit()

    # Refresh and return updated user
    await db.refresh(user)
    return user

@router.delete("/{user_id}")
async def delete_user(
    user: User = Depends(get_user_by_id),
    db: AsyncSession = Depends(get_db)
):
    await db.delete(user)
    await db.commit()
    return {"message": "User deleted successfully"}