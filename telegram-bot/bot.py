import asyncio
import logging
import json
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
import aiohttp
import os

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Конфигурация
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8496809509:AAFiyMpRpUIMLIH1V3uXldCbllmayB9P8Hs")
CHATWOOT_URL = os.getenv("CHATWOOT_URL", "http://host.docker.internal:3000")
CHATWOOT_API_TOKEN = os.getenv("CHATWOOT_API_TOKEN", "")
CHATWOOT_ACCOUNT_ID = os.getenv("CHATWOOT_ACCOUNT_ID", "1")
CHATWOOT_INBOX_ID = os.getenv("CHATWOOT_INBOX_ID", "1")

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def create_or_get_contact(phone: str, name: str = "") -> dict:
    """Создать или получить контакт в Chatwoot"""
    # #region agent log
    import time
    try:
        with open('/logs/debug.log', 'a') as f:
            f.write(json.dumps({"sessionId":"cbe068","location":"bot.py:26","message":"create_or_get_contact entry","data":{"phone":phone,"name":name,"api_token_len":len(CHATWOOT_API_TOKEN),"account_id":CHATWOOT_ACCOUNT_ID,"url":CHATWOOT_URL},"timestamp":int(time.time()*1000),"runId":"run1","hypothesisId":"A-C"}) + '\n')
    except: pass
    # #endregion
    
    async with aiohttp.ClientSession() as session:
        # Поиск контакта
        search_url = f"{CHATWOOT_URL}/api/v1/accounts/{CHATWOOT_ACCOUNT_ID}/contacts/search"
        headers = {"api_access_token": CHATWOOT_API_TOKEN}
        params = {"q": phone}
        
        # #region agent log
        try:
            with open('/logs/debug.log', 'a') as f:
                f.write(json.dumps({"sessionId":"cbe068","location":"bot.py:34","message":"search contact request","data":{"url":search_url,"has_token":bool(CHATWOOT_API_TOKEN)},"timestamp":int(time.time()*1000),"runId":"run1","hypothesisId":"B"}) + '\n')
        except: pass
        # #endregion
        
        async with session.get(search_url, headers=headers, params=params) as resp:
            # #region agent log
            resp_text = await resp.text()
            try:
                with open('/logs/debug.log', 'a') as f:
                    f.write(json.dumps({"sessionId":"cbe068","location":"bot.py:38","message":"search contact response","data":{"status":resp.status,"response":resp_text[:200]},"timestamp":int(time.time()*1000),"runId":"run1","hypothesisId":"A-B"}) + '\n')
            except: pass
            # #endregion
            if resp.status == 200:
                data = json.loads(resp_text)
                if data.get("payload"):
                    return data["payload"][0]
        
        # Создать новый контакт
        create_url = f"{CHATWOOT_URL}/api/v1/accounts/{CHATWOOT_ACCOUNT_ID}/contacts"
        contact_data = {
            "name": name or f"User {phone}",
            "identifier": phone
        }
        
        async with session.post(create_url, headers=headers, json=contact_data) as resp:
            # #region agent log
            resp_text = await resp.text()
            try:
                with open('/logs/debug.log', 'a') as f:
                    f.write(json.dumps({"sessionId":"cbe068","location":"bot.py:52","message":"create contact response","data":{"status":resp.status,"response":resp_text[:300]},"timestamp":int(time.time()*1000),"runId":"run1","hypothesisId":"D"}) + '\n')
            except: pass
            # #endregion
            if resp.status == 200:
                data = json.loads(resp_text)
                return data.get("payload", {})
            else:
                logger.error(f"Failed to create contact: {resp.status}")
                return {}


async def get_or_create_conversation(contact_id: int, source_id: str) -> dict:
    """Получить существующую или создать новую беседу в Chatwoot"""
    # #region agent log
    import time
    try:
        with open('/logs/debug.log', 'a') as f:
            f.write(json.dumps({"sessionId":"cbe068","location":"bot.py:57","message":"get_or_create_conversation entry","data":{"contact_id":contact_id,"source_id":source_id,"inbox_id":CHATWOOT_INBOX_ID},"timestamp":int(time.time()*1000),"runId":"run1","hypothesisId":"G"}) + '\n')
    except: pass
    # #endregion
    
    async with aiohttp.ClientSession() as session:
        # Сначала ищем существующую открытую беседу для этого контакта
        search_url = f"{CHATWOOT_URL}/api/v1/accounts/{CHATWOOT_ACCOUNT_ID}/conversations"
        headers = {"api_access_token": CHATWOOT_API_TOKEN}
        params = {"inbox_id": CHATWOOT_INBOX_ID, "status": "open"}
        
        # #region agent log
        try:
            with open('/logs/debug.log', 'a') as f:
                f.write(json.dumps({"sessionId":"cbe068","location":"bot.py:69","message":"searching existing conversations","data":{"url":search_url,"params":params},"timestamp":int(time.time()*1000),"runId":"run1","hypothesisId":"G"}) + '\n')
        except: pass
        # #endregion
        
        async with session.get(search_url, headers=headers, params=params) as resp:
            if resp.status == 200:
                data = await resp.json()
                conversations = data.get("data", {}).get("payload", [])
                
                # #region agent log
                try:
                    with open('/logs/debug.log', 'a') as f:
                        f.write(json.dumps({"sessionId":"cbe068","location":"bot.py:77","message":"found conversations","data":{"count":len(conversations),"contact_id":contact_id},"timestamp":int(time.time()*1000),"runId":"run1","hypothesisId":"G"}) + '\n')
                except: pass
                # #endregion
                
                # Ищем беседу для этого контакта
                for conv in conversations:
                    if conv.get("meta", {}).get("sender", {}).get("id") == contact_id:
                        # #region agent log
                        try:
                            with open('/logs/debug.log', 'a') as f:
                                f.write(json.dumps({"sessionId":"cbe068","location":"bot.py:85","message":"reusing existing conversation","data":{"conversation_id":conv.get("id")},"timestamp":int(time.time()*1000),"runId":"run1","hypothesisId":"G"}) + '\n')
                        except: pass
                        # #endregion
                        logger.info(f"Reusing existing conversation {conv.get('id')}")
                        return conv
        
        # Если не нашли - создаем новую
        # #region agent log
        try:
            with open('/logs/debug.log', 'a') as f:
                f.write(json.dumps({"sessionId":"cbe068","location":"bot.py:93","message":"creating new conversation","data":{"contact_id":contact_id},"timestamp":int(time.time()*1000),"runId":"run1","hypothesisId":"G"}) + '\n')
        except: pass
        # #endregion
        
        url = f"{CHATWOOT_URL}/api/v1/accounts/{CHATWOOT_ACCOUNT_ID}/conversations"
        conv_data = {
            "source_id": source_id,
            "inbox_id": CHATWOOT_INBOX_ID,
            "contact_id": contact_id,
            "status": "open"
        }
        
        async with session.post(url, headers=headers, json=conv_data) as resp:
            # #region agent log
            resp_text = await resp.text()
            try:
                with open('/logs/debug.log', 'a') as f:
                    f.write(json.dumps({"sessionId":"cbe068","location":"bot.py:108","message":"create_conversation response","data":{"status":resp.status,"response":resp_text[:300]},"timestamp":int(time.time()*1000),"runId":"run1","hypothesisId":"G"}) + '\n')
            except: pass
            # #endregion
            if resp.status == 200:
                data = json.loads(resp_text)
                return data
            else:
                error_text = resp_text
                logger.error(f"Failed to create conversation: {resp.status}, {error_text}")
                return {}


async def send_to_chatwoot(message: Message):
    """Отправить сообщение в Chatwoot"""
    try:
        phone = str(message.from_user.id)
        name = message.from_user.full_name or message.from_user.username or ""
        
        # Получить или создать контакт
        contact = await create_or_get_contact(phone, name)
        if not contact:
            logger.error("Failed to get or create contact")
            return
        
        contact_id = contact.get("id")
        
        # Получить или создать беседу
        conversation = await get_or_create_conversation(contact_id, f"telegram_{message.from_user.id}")
        if not conversation:
            logger.error("Failed to create conversation")
            return
        
        conversation_id = conversation.get("id")
        
        # #region agent log
        try:
            with open('/logs/debug.log', 'a') as f:
                f.write(json.dumps({"sessionId":"cbe068","location":"bot.py:149","message":"about to send message","data":{"conversation_id":conversation_id,"has_text":bool(message.text),"text_len":len(message.text) if message.text else 0},"timestamp":int(time.time()*1000),"runId":"run1","hypothesisId":"F"}) + '\n')
        except: pass
        # #endregion
        
        # Отправить сообщение
        async with aiohttp.ClientSession() as session:
            url = f"{CHATWOOT_URL}/api/v1/accounts/{CHATWOOT_ACCOUNT_ID}/conversations/{conversation_id}/messages"
            headers = {"api_access_token": CHATWOOT_API_TOKEN}
            msg_data = {
                "content": message.text,
                "message_type": "incoming",
                "private": False
            }
            
            # #region agent log
            try:
                with open('/logs/debug.log', 'a') as f:
                    f.write(json.dumps({"sessionId":"cbe068","location":"bot.py:161","message":"sending message request","data":{"url":url,"msg_data":msg_data},"timestamp":int(time.time()*1000),"runId":"run1","hypothesisId":"F"}) + '\n')
            except: pass
            # #endregion
            
            async with session.post(url, headers=headers, json=msg_data) as resp:
                # #region agent log
                resp_text = await resp.text()
                try:
                    with open('/logs/debug.log', 'a') as f:
                        f.write(json.dumps({"sessionId":"cbe068","location":"bot.py:169","message":"send message response","data":{"status":resp.status,"response":resp_text[:300]},"timestamp":int(time.time()*1000),"runId":"run1","hypothesisId":"F"}) + '\n')
                except: pass
                # #endregion
                if resp.status == 200:
                    logger.info(f"Message sent to Chatwoot: {message.text[:50]}")
                else:
                    error_text = resp_text
                    logger.error(f"Failed to send message: {resp.status}, {error_text}")
    
    except Exception as e:
        logger.error(f"Error sending to Chatwoot: {e}")


@dp.message(Command("start"))
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    welcome_text = """👋 Добро пожаловать в MEDLIFT connect!

Семья Медицинский центр - ваш персональный медицинский ассистент. 

Задайте мне любой вопрос о медицине, и я постараюсь помочь.

Наши специалисты также получат ваше сообщение и ответят в ближайшее время."""
    
    await message.answer(welcome_text)
    await send_to_chatwoot(message)


@dp.message()
async def handle_message(message: Message):
    """Обработчик всех сообщений"""
    # Отправить в Chatwoot
    await send_to_chatwoot(message)
    
    # Отправить подтверждение пользователю
    await message.answer("✅ Ваше сообщение получено! Наш специалист ответит в ближайшее время.")


async def main():
    """Запуск бота"""
    logger.info("Starting MedConnect Telegram Bot...")
    logger.info(f"Chatwoot URL: {CHATWOOT_URL}")
    logger.info(f"Account ID: {CHATWOOT_ACCOUNT_ID}")
    logger.info(f"Inbox ID: {CHATWOOT_INBOX_ID}")
    
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
