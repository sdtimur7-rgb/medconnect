from datetime import datetime, timedelta
from typing import List

from core.logging import setup_logging
from db.models import Appointment

logger = setup_logging()


async def send_reminder_24h(appointment: Appointment):
    logger.info(f"Sending 24h reminder for appointment {appointment.id}")


async def send_reminder_2h(appointment: Appointment):
    logger.info(f"Sending 2h reminder for appointment {appointment.id}")


async def send_sms_reminder(phone: str, message: str):
    logger.info(f"Sending SMS to {phone}: {message}")


def format_reminder_message(appointment: Appointment) -> str:
    return f"""Добрый день, {appointment.patient.full_name}!

Напоминаем о вашей записи:
📅 {appointment.appointment_time.strftime('%d.%m.%Y в %H:%M')}
👨‍⚕️ {appointment.doctor_name} — {appointment.specialty}

Пожалуйста, подтвердите визит:"""
