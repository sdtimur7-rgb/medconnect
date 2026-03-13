from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
import redis.asyncio as redis

from api.dependencies import get_db_session
from core.config import settings

router = APIRouter()


@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db_session)):
    try:
        await db.execute("SELECT 1")
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    try:
        redis_client = redis.from_url(settings.REDIS_URL)
        await redis_client.ping()
        redis_status = "healthy"
        await redis_client.close()
    except Exception as e:
        redis_status = f"unhealthy: {str(e)}"
    
    return {
        "status": "ok" if db_status == "healthy" and redis_status == "healthy" else "degraded",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "database": db_status,
            "redis": redis_status,
        }
    }
