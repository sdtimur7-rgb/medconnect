from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from core.logging import setup_logging

logger = setup_logging()
router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    logger.info(f"User {message.from_user.id} started bot")
    
    await message.answer(
        f"Добро пожаловать в MedConnect!\n\n"
        f"Я помогу вам управлять записями к врачам.\n\n"
        f"Ваш Telegram ID: {message.from_user.id}"
    )


@router.callback_query(lambda c: c.data and c.data.startswith("confirm_"))
async def process_confirmation(callback: types.CallbackQuery):
    appointment_id = callback.data.split("_")[1]
    logger.info(f"User {callback.from_user.id} confirmed appointment {appointment_id}")
    
    await callback.message.edit_text(
        "✅ Отлично! Ваша запись подтверждена. Ждём вас!",
    )
    await callback.answer("Запись подтверждена")


@router.callback_query(lambda c: c.data and c.data.startswith("cancel_"))
async def process_cancellation(callback: types.CallbackQuery):
    appointment_id = callback.data.split("_")[1]
    logger.info(f"User {callback.from_user.id} cancelled appointment {appointment_id}")
    
    await callback.message.edit_text(
        "Запись отменена. Наш менеджер свяжется с вами для переноса.",
    )
    await callback.answer("Запись отменена")


@router.callback_query(lambda c: c.data == "call_us")
async def process_call_request(callback: types.CallbackQuery):
    logger.info(f"User {callback.from_user.id} requested a call")
    
    await callback.message.answer(
        "Наш менеджер свяжется с вами в ближайшее время."
    )
    await callback.answer("Запрос принят")


@router.message()
async def handle_message(message: types.Message):
    logger.info(f"Message from {message.from_user.id}: {message.text}")
    
    await message.answer(
        "Я передал ваше сообщение менеджеру. Он ответит в ближайшее время."
    )
