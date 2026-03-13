from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_confirmation_keyboard(appointment_id: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Подтверждаю", callback_data=f"confirm_{appointment_id}"),
            InlineKeyboardButton(text="❌ Отменяю", callback_data=f"cancel_{appointment_id}")
        ],
        [
            InlineKeyboardButton(text="📞 Позвонить нам", callback_data="call_us")
        ]
    ])
    return keyboard
