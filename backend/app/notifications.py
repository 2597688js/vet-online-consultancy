import smtplib
from email.message import EmailMessage

from sqlalchemy.orm import Session

from app.config import settings
from app.models import Appointment, User, UserRole


def send_appointment_reminder(db: Session, appointment: Appointment) -> bool:
    """Returns True if an email was actually sent."""
    if not settings.smtp_host:
        return False

    recipients = (
        db.query(User)
        .filter(User.role.in_((UserRole.ADMIN, UserRole.VET)), User.is_active.is_(True), User.deleted_at.is_(None))
        .all()
    )
    if not recipients:
        return False

    dashboard_url = f"{settings.app_base_url.rstrip('/')}/admin"
    start_time = appointment.scheduled_start.strftime("%b %d, %Y at %I:%M %p")
    body = (
        f"Upcoming consultation in 15 minutes:\n\n"
        f"Pet: {appointment.pet.name} ({appointment.pet.species})\n"
        f"Owner: {appointment.owner.full_name}\n"
        f"Phone: {appointment.owner.phone or 'not provided'}\n"
        f"Time: {start_time}\n"
        f"Symptoms: {appointment.symptoms or 'none noted'}\n\n"
        f"Open the dashboard: {dashboard_url}"
    )

    message = EmailMessage()
    message["Subject"] = f"Consultation in 15 min: {appointment.pet.name} ({appointment.owner.full_name})"
    message["From"] = settings.smtp_from_email or settings.smtp_username
    message["To"] = ", ".join(user.email for user in recipients)
    message.set_content(body)

    with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as smtp:
        smtp.starttls()
        if settings.smtp_username:
            smtp.login(settings.smtp_username, settings.smtp_password)
        smtp.send_message(message)
    return True
