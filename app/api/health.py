from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import HealthCheckResponse
from app.database import get_db, health_check
from app.config import settings

router = APIRouter(tags=["Health"])

@router.get("/health", response_model=HealthCheckResponse)
async def health_check_route(db: AsyncSession = Depends(get_db)):
    db_healthy = await health_check()
    return HealthCheckResponse(
        status="healthy" if db_healthy else "unhealthy",
        database="connected" if db_healthy else "disconnected",
        timestamp=datetime.now(),
        environment=settings.app_env
    )