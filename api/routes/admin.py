from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

from api.dependencies import get_db_session
from db.crud import CenterCRUD
from db.models import Center

router = APIRouter()


class CenterCreate(BaseModel):
    name: str
    slug: str
    telegram_bot_token: Optional[str] = None
    onec_api_url: Optional[str] = None
    onec_api_key: Optional[str] = None
    sms_enabled: bool = True
    price_per_confirmation: float = 50.00
    center_info: Optional[str] = None


class CenterResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    is_active: bool
    price_per_confirmation: float
    
    class Config:
        from_attributes = True


@router.post("/centers", response_model=CenterResponse)
async def create_center(
    center_data: CenterCreate,
    db: AsyncSession = Depends(get_db_session)
):
    existing = await CenterCRUD.get_by_slug(db, center_data.slug)
    if existing:
        raise HTTPException(status_code=400, detail="Center with this slug already exists")
    
    center = await CenterCRUD.create(db, **center_data.dict())
    await db.commit()
    
    return center


@router.get("/centers", response_model=List[CenterResponse])
async def list_centers(db: AsyncSession = Depends(get_db_session)):
    centers = await CenterCRUD.get_active(db)
    return centers
