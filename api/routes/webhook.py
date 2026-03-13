from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional

from api.dependencies import get_db_session
from core.logging import setup_logging

router = APIRouter()
logger = setup_logging()


class ChatwootWebhook(BaseModel):
    event: str
    conversation_id: Optional[int] = None
    message_id: Optional[int] = None
    content: Optional[str] = None
    sender_type: Optional[str] = None


@router.post("/chatwoot")
async def chatwoot_webhook(
    webhook: ChatwootWebhook,
    db: AsyncSession = Depends(get_db_session)
):
    logger.info(f"Received Chatwoot webhook: {webhook.event}")
    
    if webhook.event == "message_created" and webhook.sender_type == "agent":
        logger.info(f"Agent message: {webhook.content}")
    
    return {"status": "ok"}
