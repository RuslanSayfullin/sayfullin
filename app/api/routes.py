from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.schemas import StatsResponse
from app.database import get_db
from app.models import User, Post

router = APIRouter()

@router.get("/")
async def root():
    return {
        "message": "FastAPI with SQLAlchemy, AsyncPG and PostgreSQL",
        "status": "success",
        "timestamp": datetime.now()
    }

@router.get("/stats", response_model=StatsResponse)
async def get_stats(db: AsyncSession = Depends(get_db)):
    # Total users
    users_count = await db.execute(select(func.count(User.id)))
    total_users = users_count.scalar()

    # Total posts
    posts_count = await db.execute(select(func.count(Post.id)))
    total_posts = posts_count.scalar()

    # Average name length
    avg_name_length = await db.execute(select(func.avg(func.length(User.name))))
    avg_name = avg_name_length.scalar() or 0

    # First and last user dates
    dates = await db.execute(
        select(
            func.min(User.created_at).label("first_date"),
            func.max(User.created_at).label("last_date")
        )
    )
    dates_result = dates.first()

    return StatsResponse(
        total_users=total_users,
        total_posts=total_posts,
        avg_name_length=float(avg_name),
        first_user_date=dates_result.first_date,
        last_user_date=dates_result.last_date,
    )