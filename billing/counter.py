from datetime import datetime
from typing import Dict
from uuid import UUID

from core.logging import setup_logging

logger = setup_logging()


class BillingCounter:
    @staticmethod
    async def record_confirmation(
        db,
        center_id: UUID,
        appointment_id: UUID,
        amount: float
    ) -> Dict:
        from db.crud import BillingEventCRUD
        
        event = await BillingEventCRUD.create(
            db,
            center_id=center_id,
            appointment_id=appointment_id,
            amount=amount
        )
        
        logger.info(f"Recorded billing event: {event.id} for {amount} RUB")
        
        return {
            "event_id": str(event.id),
            "amount": float(amount),
            "billed_at": event.billed_at.isoformat()
        }
