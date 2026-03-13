from aiogram import Router, types
from aiogram.filters import Command

from core.config import settings
from core.logging import setup_logging

logger = setup_logging()
router = Router()


def is_admin(user_id: int) -> bool:
    return user_id == settings.ADMIN_TELEGRAM_ID


@router.message(Command("admin"))
async def cmd_admin(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("У вас нет прав администратора")
        return
    
    await message.answer(
        "Панель администратора MedConnect\n\n"
        "Доступные команды:\n"
        "/stats - Статистика\n"
        "/centers - Список центров"
    )


@router.message(Command("stats"))
async def cmd_stats(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    
    await message.answer(
        "Статистика системы:\n\n"
        "Центров: 0\n"
        "Пациентов: 0\n"
        "Записей: 0\n"
        "Подтверждений: 0"
    )
