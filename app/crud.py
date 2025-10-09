from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import User
from app.schemas import UserCreate, UserUpdate

class CRUDUser:
    async def get(self, db: AsyncSession, user_id: int) -> Optional[User]:
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
    
    async def get_by_username(self, db: AsyncSession, username: str) -> Optional[User]:
        result = await db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()
    
    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
    
    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
        result = await db.execute(select(User).offset(skip).limit(limit))
        return result.scalars().all()
    
    async def create(self, db: AsyncSession, user_in: UserCreate) -> User:
        db_user = User(**user_in.model_dump())
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    
    async def update(self, db: AsyncSession, user_id: int, user_in: UserUpdate) -> Optional[User]:
        user = await self.get(db, user_id)
        if user:
            update_data = user_in.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(user, field, value)
            await db.commit()
            await db.refresh(user)
        return user
    
    async def delete(self, db: AsyncSession, user_id: int) -> Optional[User]:
        user = await self.get(db, user_id)
        if user:
            await db.delete(user)
            await db.commit()
        return User


user = CRUDUser()