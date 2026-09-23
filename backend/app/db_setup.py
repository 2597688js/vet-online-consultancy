"""Brings the database up to date on startup: creates it if missing, then runs migrations."""
import logging

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url

from app.config import BACKEND_DIR, settings

logger = logging.getLogger(__name__)


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


def prepare_database() -> None:
    _create_database_if_missing()
    config = Config(str(BACKEND_DIR / "alembic.ini"))
    config.attributes["configure_logger"] = False  # keep uvicorn's logging intact
    command.upgrade(config, "head")
