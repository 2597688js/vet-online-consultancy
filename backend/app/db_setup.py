"""Startup tasks: create the database if missing, run migrations, make sure the doctor exists."""
import logging

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url

from app.config import BACKEND_DIR, settings
from app.database import SessionLocal
from app.models import DoctorProfile, User, UserRole, VerificationStatus

logger = logging.getLogger("uvicorn.error")

DOCTOR_NAME = "Dr. Nituparna Sarkar"


def _create_database_if_missing() -> None:
    url = make_url(settings.database_url)
    admin_engine = create_engine(url.set(database="postgres"), isolation_level="AUTOCOMMIT")
    try:
        with admin_engine.connect() as conn:
            exists = conn.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :name"), {"name": url.database}
            ).scalar()
            if not exists:
                conn.execute(text(f'CREATE DATABASE "{url.database}"'))
                logger.info("Created database %s", url.database)
    except Exception as exc:  # no rights on the "postgres" db etc. — migrations will report real problems
        logger.warning("Could not check/create database %s: %s", url.database, exc)
    finally:
        admin_engine.dispose()


def _ensure_doctor() -> None:
    """Bookings need the doctor's profile. Create it on first run; keep her email in sync with DOCTOR_EMAIL."""
    with SessionLocal() as db:
        doctor = db.query(DoctorProfile).order_by(DoctorProfile.created_at.asc()).first()
        if doctor is None:
            user = User(
                full_name=DOCTOR_NAME,
                email=settings.doctor_email or "doctor@example.com",
                role=UserRole.ADMIN,
                is_active=True,
            )
            db.add(user)
            db.flush()
            db.add(
                DoctorProfile(
                    user_id=user.id,
                    specialty="General Veterinary Medicine",
                    verification_status=VerificationStatus.VERIFIED,
                    is_accepting_appointments=True,
                )
            )
            logger.info("Created doctor profile for %s", DOCTOR_NAME)
        elif settings.doctor_email and doctor.user.email != settings.doctor_email:
            doctor.user.email = settings.doctor_email
        db.commit()


def prepare_database() -> None:
    _create_database_if_missing()
    config = Config(str(BACKEND_DIR / "alembic.ini"))
    config.attributes["configure_logger"] = False  # keep uvicorn's logging intact
    command.upgrade(config, "head")
    _ensure_doctor()
    logger.info("Admin dashboard: %s/admin", settings.app_base_url.rstrip("/"))
