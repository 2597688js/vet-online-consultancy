import smtplib
from email.message import EmailMessage

from app.config import settings
from app.models import Appointment


def send_appointment_reminder(appointment: Appointment) -> bool:
    """Email the doctor (DOCTOR_EMAIL). Returns True if an email was actually sent."""
    if not settings.smtp_host or not settings.doctor_email:
        return False

    dashboard_url = f"{settings.app_base_url.rstrip('/')}/admin"
    start_time = appointment.scheduled_start.strftime("%b %d, %Y at %I:%M %p")
    pet_label = appointment.pet.name or "Unnamed pet"
    owner_name = appointment.contact_name or appointment.owner.full_name
    owner_phone = appointment.contact_phone or appointment.owner.phone
    body = (
        f"Upcoming consultation in 15 minutes:\n\n"
        f"Pet: {pet_label} ({appointment.pet.species})\n"
        f"Owner: {owner_name}\n"
        f"Phone: {owner_phone or 'not provided'}\n"
        f"Time: {start_time}\n"
        f"Main problem: {appointment.symptoms or 'none noted'}\n\n"
        f"Open the dashboard: {dashboard_url}"
    )

    message = EmailMessage()
    message["Subject"] = f"Consultation in 15 min: {pet_label} ({owner_name})"
    message["From"] = settings.smtp_from_email or settings.smtp_username
    message["To"] = settings.doctor_email
    message.set_content(body)

    with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as smtp:
        smtp.starttls()
        if settings.smtp_username:
            smtp.login(settings.smtp_username, settings.smtp_password)
        smtp.send_message(message)
    return True
