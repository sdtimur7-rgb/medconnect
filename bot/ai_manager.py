from anthropic import Anthropic
from typing import List, Dict, Optional

from core.config import settings
from core.exceptions import AIManagerException
from core.logging import setup_logging

logger = setup_logging()


class AIManager:
    def __init__(self, center_info: str = ""):
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.center_info = center_info
        self.system_prompt = self._build_system_prompt()
    
    def _build_system_prompt(self) -> str:
        return f"""
Ты вежливый медицинский администратор клиники.
Твоя задача — отвечать пациентам в Telegram.

Ты умеешь:
- Отвечать на вопросы о подготовке к приёму
- Помогать перенести запись (уточни удобное время и передай менеджеру)
- Отвечать на вопросы о документах и анализах
- Сообщать адрес и контакты клиники

Ты НЕ умеешь:
- Ставить диагнозы
- Давать медицинские советы
- Называть цены (направляй к менеджеру)

Если не знаешь ответа — скажи что передашь вопрос менеджеру.
Отвечай кратко, по-русски, дружелюбно.

Информация о клинике:
{self.center_info}
"""
    
    async def get_response(
        self,
        message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> tuple[str, bool]:
        try:
            messages = conversation_history or []
            messages.append({"role": "user", "content": message})
            
            response = self.client.messages.create(
                model=settings.ANTHROPIC_MODEL,
                max_tokens=1024,
                system=self.system_prompt,
                messages=messages
            )
            
            ai_response = response.content[0].text
            
            needs_human = any(
                keyword in ai_response.lower()
                for keyword in ["передам менеджеру", "свяжется менеджер", "уточню у менеджера"]
            )
            
            return ai_response, needs_human
            
        except Exception as e:
            logger.error(f"AI Manager error: {e}")
            raise AIManagerException(f"Failed to get AI response: {str(e)}")
