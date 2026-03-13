from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from datetime import datetime
from uuid import UUID

from db.models import Center, Patient, Appointment, BillingEvent, Invoice


class CenterCRUD:
    @staticmethod
    async def create(db: AsyncSession, **kwargs) -> Center:
        center = Center(**kwargs)
        db.add(center)
        await db.flush()
        await db.refresh(center)
        return center
    
    @staticmethod
    async def get_by_id(db: AsyncSession, center_id: UUID) -> Optional[Center]:
        result = await db.execute(select(Center).where(Center.id == center_id))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_by_slug(db: AsyncSession, slug: str) -> Optional[Center]:
        result = await db.execute(select(Center).where(Center.slug == slug))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_active(db: AsyncSession) -> List[Center]:
        result = await db.execute(select(Center).where(Center.is_active == True))
        return result.scalars().all()


class PatientCRUD:
    @staticmethod
    async def create(db: AsyncSession, **kwargs) -> Patient:
        patient = Patient(**kwargs)
        db.add(patient)
        await db.flush()
        await db.refresh(patient)
        return patient
    
    @staticmethod
    async def get_by_id(db: AsyncSession, patient_id: UUID) -> Optional[Patient]:
        result = await db.execute(select(Patient).where(Patient.id == patient_id))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_by_telegram_id(db: AsyncSession, telegram_id: int, center_id: UUID) -> Optional[Patient]:
        result = await db.execute(
            select(Patient).where(
                Patient.telegram_id == telegram_id,
                Patient.center_id == center_id
            )
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_by_phone(db: AsyncSession, phone: str, center_id: UUID) -> Optional[Patient]:
        result = await db.execute(
            select(Patient).where(
                Patient.phone == phone,
                Patient.center_id == center_id
            )
        )
        return result.scalar_one_or_none()


class AppointmentCRUD:
    @staticmethod
    async def create(db: AsyncSession, **kwargs) -> Appointment:
        appointment = Appointment(**kwargs)
        db.add(appointment)
        await db.flush()
        await db.refresh(appointment)
        return appointment
    
    @staticmethod
    async def get_by_id(db: AsyncSession, appointment_id: UUID) -> Optional[Appointment]:
        result = await db.execute(select(Appointment).where(Appointment.id == appointment_id))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_pending_reminders_24h(db: AsyncSession, time_from: datetime, time_to: datetime) -> List[Appointment]:
        result = await db.execute(
            select(Appointment).where(
                Appointment.appointment_time.between(time_from, time_to),
                Appointment.reminder_24h_sent == False,
                Appointment.status == "pending"
            )
        )
        return result.scalars().all()
    
    @staticmethod
    async def get_pending_reminders_2h(db: AsyncSession, time_from: datetime, time_to: datetime) -> List[Appointment]:
        result = await db.execute(
            select(Appointment).where(
                Appointment.appointment_time.between(time_from, time_to),
                Appointment.reminder_2h_sent == False,
                Appointment.status == "pending"
            )
        )
        return result.scalars().all()
    
    @staticmethod
    async def update_status(db: AsyncSession, appointment_id: UUID, status: str) -> Optional[Appointment]:
        appointment = await AppointmentCRUD.get_by_id(db, appointment_id)
        if appointment:
            appointment.status = status
            if status == "confirmed":
                appointment.confirmed_at = datetime.utcnow()
            await db.flush()
            await db.refresh(appointment)
        return appointment


class BillingEventCRUD:
    @staticmethod
    async def create(db: AsyncSession, **kwargs) -> BillingEvent:
        event = BillingEvent(**kwargs)
        db.add(event)
        await db.flush()
        await db.refresh(event)
        return event
    
    @staticmethod
    async def get_by_period(db: AsyncSession, center_id: UUID, start: datetime, end: datetime) -> List[BillingEvent]:
        result = await db.execute(
            select(BillingEvent).where(
                BillingEvent.center_id == center_id,
                BillingEvent.billed_at.between(start, end)
            )
        )
        return result.scalars().all()


class InvoiceCRUD:
    @staticmethod
    async def create(db: AsyncSession, **kwargs) -> Invoice:
        invoice = Invoice(**kwargs)
        db.add(invoice)
        await db.flush()
        await db.refresh(invoice)
        return invoice
    
    @staticmethod
    async def get_by_id(db: AsyncSession, invoice_id: UUID) -> Optional[Invoice]:
        result = await db.execute(select(Invoice).where(Invoice.id == invoice_id))
        return result.scalar_one_or_none()
