import httpx
from typing import Optional, Dict

from core.config import settings
from core.exceptions import SMSException
from core.logging import setup_logging

logger = setup_logging()


class SMSCenterClient:
    def __init__(self):
        self.login = settings.SMSC_LOGIN
        self.password = settings.SMSC_PASSWORD
        self.base_url = "https://smsc.ru/sys/send.php"
        self.enabled = settings.SMSC_ENABLED
    
    async def send_sms(
        self,
        phone: str,
        message: str,
        sender: Optional[str] = None
    ) -> Dict:
        if not self.enabled:
            logger.warning("SMS sending is disabled")
            return {"status": "disabled"}
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                params = {
                    "login": self.login,
                    "psw": self.password,
                    "phones": phone,
                    "mes": message,
                    "charset": "utf-8",
                    "fmt": "3",
                }
                
                if sender:
                    params["sender"] = sender
                
                response = await client.get(self.base_url, params=params)
                response.raise_for_status()
                
                result = response.json()
                
                if result.get("error"):
                    raise SMSException(f"SMS API error: {result.get('error_code')}")
                
                logger.info(f"SMS sent to {phone}, ID: {result.get('id')}")
                
                return result
                
        except httpx.HTTPError as e:
            logger.error(f"SMS sending failed: {e}")
            raise SMSException(f"Failed to send SMS: {str(e)}")
    
    async def get_balance(self) -> float:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    "https://smsc.ru/sys/balance.php",
                    params={
                        "login": self.login,
                        "psw": self.password,
                        "fmt": "3"
                    }
                )
                response.raise_for_status()
                
                result = response.json()
                balance = float(result.get("balance", 0))
                
                logger.info(f"SMS balance: {balance} RUB")
                
                return balance
                
        except Exception as e:
            logger.error(f"Failed to get SMS balance: {e}")
            return 0.0
