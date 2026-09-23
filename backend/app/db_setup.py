"""Startup tasks: start the project's Postgres, create the database if missing, run migrations, make sure the doctor exists."""
import logging
import subprocess
from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url

from app.config import BACKEND_DIR, settings
from app.database import SessionLocal
from app.models import DoctorProfile, User, UserRole, VerificationStatus

logger = logging.getLogger("uvicorn.error")

DOCTOR_NAME = "Dr. Nituparna Sarkar"
LOCAL_POSTGRES_PORT = 5433


def _start_local_postgres() -> None:
    """Run a Postgres server with its data in the project's db/ folder, creating it on first run.

    Skipped when DATABASE_URL points at any other server. The server keeps running after the backend
    stops; stop it with `pg_ctl -D db stop` from the project folder.
    """
    url = make_url(settings.database_url)
    if url.host not in ("localhost", "127.0.0.1") or url.port != LOCAL_POSTGRES_PORT:
        return

    data_dir = Path(settings.local_postgres_dir)
    if not (data_dir / "PG_VERSION").exists():
        command = ["initdb", "-D", str(data_dir), "--auth=trust", "--encoding=UTF8", "--locale=en_US.UTF-8"]
        if url.username:
            command += ["--username", url.username]
        subprocess.run(command, check=True, capture_output=True)
        with open(data_dir / "postgresql.conf", "a") as conf:
            conf.write(f"\nport = {LOCAL_POSTGRES_PORT}\n")
        logger.info("Created Postgres data folder at %s", data_dir)

    if subprocess.run(["pg_ctl", "status", "-D", str(data_dir)], capture_output=True).returncode == 0:
        return
    subprocess.run(
        ["pg_ctl", "start", "-w", "-D", str(data_dir), "-l", str(data_dir / "server.log")],
        check=True,
        capture_output=True,
    )
    logger.info("Started Postgres on port %s (data in %s)", LOCAL_POSTGRES_PORT, data_dir)


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
    _start_local_postgres()
    _create_database_if_missing()
    config = Config(str(BACKEND_DIR / "alembic.ini"))
    config.attributes["configure_logger"] = False  # keep uvicorn's logging intact
    command.upgrade(config, "head")
    _ensure_doctor()
    logger.info("Admin dashboard: %s/admin", settings.app_base_url.rstrip("/"))
