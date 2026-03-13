import httpx
from typing import Dict, Optional

from core.config import settings
from core.exceptions import ChatwootException
from core.logging import setup_logging

logger = setup_logging()


class ChatwootClient:
    def __init__(self):
        self.api_url = settings.CHATWOOT_API_URL.rstrip("/")
        self.api_token = settings.CHATWOOT_API_TOKEN
        self.account_id = settings.CHATWOOT_ACCOUNT_ID
        self.client = httpx.AsyncClient(timeout=30.0)
        self.headers = {
            "api_access_token": self.api_token,
            "Content-Type": "application/json"
        }
    
    async def create_conversation(
        self,
        contact_id: int,
        inbox_id: int,
        additional_attributes: Optional[Dict] = None
    ) -> Dict:
        try:
            payload = {
                "contact_id": contact_id,
                "inbox_id": inbox_id,
            }
            
            if additional_attributes:
                payload["additional_attributes"] = additional_attributes
            
            response = await self.client.post(
                f"{self.api_url}/api/v1/accounts/{self.account_id}/conversations",
                json=payload,
                headers=self.headers
            )
            response.raise_for_status()
            
            conversation = response.json()
            logger.info(f"Created conversation: {conversation['id']}")
            
            return conversation
            
        except httpx.HTTPError as e:
            logger.error(f"Chatwoot API request failed: {e}")
            raise ChatwootException(f"Failed to create conversation: {str(e)}")
    
    async def send_message(
        self,
        conversation_id: int,
        content: str,
        message_type: str = "outgoing"
    ) -> Dict:
        try:
            payload = {
                "content": content,
                "message_type": message_type,
                "private": False
            }
            
            response = await self.client.post(
                f"{self.api_url}/api/v1/accounts/{self.account_id}/conversations/{conversation_id}/messages",
                json=payload,
                headers=self.headers
            )
            response.raise_for_status()
            
            message = response.json()
            logger.info(f"Sent message to conversation {conversation_id}")
            
            return message
            
        except httpx.HTTPError as e:
            logger.error(f"Chatwoot API request failed: {e}")
            raise ChatwootException(f"Failed to send message: {str(e)}")
    
    async def create_contact(
        self,
        name: str,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        identifier: Optional[str] = None
    ) -> Dict:
        try:
            payload = {"name": name}
            
            if phone:
                payload["phone_number"] = phone
            if email:
                payload["email"] = email
            if identifier:
                payload["identifier"] = identifier
            
            response = await self.client.post(
                f"{self.api_url}/api/v1/accounts/{self.account_id}/contacts",
                json=payload,
                headers=self.headers
            )
            response.raise_for_status()
            
            contact = response.json()
            logger.info(f"Created contact: {contact['id']}")
            
            return contact
            
        except httpx.HTTPError as e:
            logger.error(f"Chatwoot API request failed: {e}")
            raise ChatwootException(f"Failed to create contact: {str(e)}")
    
    async def close(self):
        await self.client.aclose()
