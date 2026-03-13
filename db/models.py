from sqlalchemy import Column, String, Boolean, DateTime, DECIMAL, Integer, ForeignKey, Text, BigInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from db.database import Base


class Center(Base):
    __tablename__ = "centers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    telegram_bot_token = Column(String(255), nullable=True)
    onec_api_url = Column(String(500), nullable=True)
    onec_api_key = Column(String(255), nullable=True)
    sms_enabled = Column(Boolean, default=True)
    price_per_confirmation = Column(DECIMAL(10, 2), default=50.00)
    is_active = Column(Boolean, default=True)
    center_info = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    patients = relationship("Patient", back_populates="center")
    appointments = relationship("Appointment", back_populates="center")
    billing_events = relationship("BillingEvent", back_populates="center")
    invoices = relationship("Invoice", back_populates="center")


class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    center_id = Column(UUID(as_uuid=True), ForeignKey("centers.id"), nullable=False)
    telegram_id = Column(BigInteger, nullable=True)
    phone = Column(String(20), nullable=True)
    full_name = Column(String(255), nullable=True)
    onec_patient_id = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    center = relationship("Center", back_populates="patients")
    appointments = relationship("Appointment", back_populates="patient")


class Appointment(Base):
    __tablename__ = "appointments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    center_id = Column(UUID(as_uuid=True), ForeignKey("centers.id"), nullable=False)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)
    onec_appointment_id = Column(String(100), unique=True, nullable=True)
    doctor_name = Column(String(255), nullable=True)
    specialty = Column(String(255), nullable=True)
    appointment_time = Column(DateTime(timezone=True), nullable=False)
    status = Column(String(50), default="pending")
    reminder_24h_sent = Column(Boolean, default=False)
    reminder_2h_sent = Column(Boolean, default=False)
    confirmed_at = Column(DateTime(timezone=True), nullable=True)
    confirmation_channel = Column(String(20), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    center = relationship("Center", back_populates="appointments")
    patient = relationship("Patient", back_populates="appointments")
    billing_events = relationship("BillingEvent", back_populates="appointment")


class BillingEvent(Base):
    __tablename__ = "billing_events"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    center_id = Column(UUID(as_uuid=True), ForeignKey("centers.id"), nullable=False)
    appointment_id = Column(UUID(as_uuid=True), ForeignKey("appointments.id"), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    billed_at = Column(DateTime(timezone=True), server_default=func.now())
    
    center = relationship("Center", back_populates="billing_events")
    appointment = relationship("Appointment", back_populates="billing_events")


class Invoice(Base):
    __tablename__ = "invoices"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    center_id = Column(UUID(as_uuid=True), ForeignKey("centers.id"), nullable=False)
    period_start = Column(DateTime(timezone=True), nullable=False)
    period_end = Column(DateTime(timezone=True), nullable=False)
    total_confirmations = Column(Integer, default=0)
    total_amount = Column(DECIMAL(10, 2), default=0.00)
    status = Column(String(50), default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    center = relationship("Center", back_populates="invoices")
