import logging
from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler

from app.database import SessionLocal
from app.models import Appointment, AppointmentStatus
from app.notifications import send_appointment_reminder

logger = logging.getLogger(__name__)

REMINDER_WINDOW_MINUTES = 15
ACTIONABLE_STATUSES = (AppointmentStatus.PENDING, AppointmentStatus.CONFIRMED)


def check_upcoming_appointments() -> None:
    db = SessionLocal()
    try:
        now = datetime.now()
        window_end = now + timedelta(minutes=REMINDER_WINDOW_MINUTES)
        due = (
            db.query(Appointment)
            .filter(
                Appointment.status.in_(ACTIONABLE_STATUSES),
                Appointment.scheduled_start > now,
                Appointment.scheduled_start <= window_end,
                Appointment.reminder_sent_at.is_(None),
            )
            .all()
        )
        for appointment in due:
            try:
                sent = send_appointment_reminder(db, appointment)
            except Exception:
                logger.exception("Failed to send reminder for appointment %s", appointment.id)
                continue
            if sent:
                appointment.reminder_sent_at = now
        db.commit()
    finally:
        db.close()


def start_scheduler() -> BackgroundScheduler:
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_upcoming_appointments, "interval", seconds=60, id="appointment_reminders")
    scheduler.start()
    return scheduler
