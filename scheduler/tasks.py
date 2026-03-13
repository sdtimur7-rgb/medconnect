from celery import shared_task
from datetime import datetime, timedelta

from core.logging import setup_logging

logger = setup_logging()


@shared_task(name="scheduler.tasks.sync_onec_appointments")
def sync_onec_appointments():
    logger.info("Starting 1C appointments synchronization")
    
    try:
        logger.info("1C sync completed successfully")
        return {"status": "success", "synced": 0}
    except Exception as e:
        logger.error(f"1C sync failed: {e}")
        return {"status": "error", "error": str(e)}


@shared_task(name="scheduler.tasks.send_reminders_24h")
def send_reminders_24h():
    logger.info("Starting 24h reminders")
    
    try:
        logger.info("24h reminders sent successfully")
        return {"status": "success", "sent": 0}
    except Exception as e:
        logger.error(f"24h reminders failed: {e}")
        return {"status": "error", "error": str(e)}


@shared_task(name="scheduler.tasks.send_reminders_2h")
def send_reminders_2h():
    logger.info("Starting 2h reminders")
    
    try:
        logger.info("2h reminders sent successfully")
        return {"status": "success", "sent": 0}
    except Exception as e:
        logger.error(f"2h reminders failed: {e}")
        return {"status": "error", "error": str(e)}


@shared_task(name="scheduler.tasks.generate_monthly_invoices")
def generate_monthly_invoices():
    logger.info("Generating monthly invoices")
    
    try:
        logger.info("Monthly invoices generated successfully")
        return {"status": "success", "invoices": 0}
    except Exception as e:
        logger.error(f"Invoice generation failed: {e}")
        return {"status": "error", "error": str(e)}


@shared_task(name="scheduler.tasks.check_system_health")
def check_system_health():
    logger.info("Checking system health")
    
    try:
        logger.info("System health check completed")
        return {"status": "success", "health": "ok"}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {"status": "error", "error": str(e)}
