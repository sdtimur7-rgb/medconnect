from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from typing import List
from pydantic import BaseModel
from uuid import UUID

from api.dependencies import get_db_session
from db.crud import BillingEventCRUD, InvoiceCRUD

router = APIRouter()


class BillingReport(BaseModel):
    center_id: UUID
    period_start: datetime
    period_end: datetime
    total_confirmations: int
    total_amount: float


@router.get("/report/{center_id}")
async def get_billing_report(
    center_id: UUID,
    db: AsyncSession = Depends(get_db_session)
):
    now = datetime.utcnow()
    start = datetime(now.year, now.month, 1)
    if now.month == 12:
        end = datetime(now.year + 1, 1, 1)
    else:
        end = datetime(now.year, now.month + 1, 1)
    
    events = await BillingEventCRUD.get_by_period(db, center_id, start, end)
    
    total_amount = sum(float(event.amount) for event in events)
    
    return {
        "center_id": str(center_id),
        "period_start": start.isoformat(),
        "period_end": end.isoformat(),
        "total_confirmations": len(events),
        "total_amount": total_amount,
    }
