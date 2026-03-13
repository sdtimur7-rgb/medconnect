import httpx
from typing import List, Dict, Optional
from datetime import datetime

from core.config import settings
from core.exceptions import OneCAPIException
from core.logging import setup_logging

logger = setup_logging()


class OneCClient:
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url.rstrip("/")
        self.api_key = api_key
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def get_appointments(
        self,
        date_from: datetime,
        date_to: datetime
    ) -> List[Dict]:
        try:
            response = await self.client.get(
                f"{self.api_url}/api/appointments",
                params={
                    "date_from": date_from.isoformat(),
                    "date_to": date_to.isoformat()
                },
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Fetched {len(data)} appointments from 1C")
            
            return data
            
        except httpx.HTTPError as e:
            logger.error(f"1C API request failed: {e}")
            raise OneCAPIException(f"Failed to fetch appointments: {str(e)}")
    
    async def get_patient(self, patient_id: str) -> Optional[Dict]:
        try:
            response = await self.client.get(
                f"{self.api_url}/api/patients/{patient_id}",
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            response.raise_for_status()
            
            return response.json()
            
        except httpx.HTTPError as e:
            logger.error(f"1C API request failed: {e}")
            raise OneCAPIException(f"Failed to fetch patient: {str(e)}")
    
    async def close(self):
        await self.client.aclose()
