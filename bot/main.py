import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from core.config import settings
from core.logging import setup_logging
from bot.handlers import patient, admin

logger = setup_logging()


async def main():
    logger.info("Starting MedConnect Telegram Bot")
    
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    
    redis = Redis.from_url(settings.REDIS_URL)
    storage = RedisStorage(redis=redis)
    
    dp = Dispatcher(storage=storage)
    
    dp.include_router(patient.router)
    dp.include_router(admin.router)
    
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()
        await redis.close()


if __name__ == "__main__":
    asyncio.run(main())
