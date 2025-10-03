from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from app.schemas import Post, PostCreate, PostUpdate, PostWithUser
from app.database import get_db
from app.models import User
from app.dependencies import get_user_by_id, get_post_by_id

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
async def create_post(
    post: PostCreate, 
    db: AsyncSession = Depends(get_db)
):
    # Verify author exists
    result = await db.execute(select(User).where(User.id == post.author_id))
    author = result.scalar_one_or_none()

    if not author:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Author with id {post.author_id} does not exist"
        )
    
    db_post = Post(**post.model_dump())
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post

@router.get("/", response_model=List[PostWithUser])
async def read_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Post)
        .options(selectinload(Post.author))
        .order_by(Post.create_at.desc())
        .offset(skip)
        .limit(limit)
    )
    posts = result.scalars().all()
    return posts


@router.get("/{post_id}", response_model=PostWithUser)
async def read_post(post: Post = Depends(get_post_by_id)):
    return post