from celery import Celery
from celery.schedules import crontab

from core.config import settings

celery_app = Celery(
    "medconnect",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["scheduler.tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

celery_app.conf.beat_schedule = {
    "sync-1c-appointments": {
        "task": "scheduler.tasks.sync_onec_appointments",
        "schedule": 900.0,
    },
    "send-reminders-24h": {
        "task": "scheduler.tasks.send_reminders_24h",
        "schedule": 1800.0,
    },
    "send-reminders-2h": {
        "task": "scheduler.tasks.send_reminders_2h",
        "schedule": 1800.0,
    },
    "generate-monthly-invoices": {
        "task": "scheduler.tasks.generate_monthly_invoices",
        "schedule": crontab(day_of_month="1", hour="3", minute="0"),
    },
    "check-system-health": {
        "task": "scheduler.tasks.check_system_health",
        "schedule": 600.0,
    },
}
