"""Create or update Dr. Nituparna Sarkar's admin account.

This is a data seed, not a schema migration — it reuses the existing
users / doctor_profiles tables as-is. Safe to re-run: it upserts by email.

Usage:
    cd backend
    source .venv/bin/activate
    ADMIN_EMAIL=nituparna@example.com ADMIN_PASSWORD='a-strong-password' python -m scripts.seed_admin
"""
import os
import sys

from app.database import SessionLocal
from app.db_setup import prepare_database
from app.models import DoctorProfile, User, UserRole, VerificationStatus
from app.security import hash_password

DOCTOR_NAME = "Dr. Nituparna Sarkar"


def main() -> None:
    email = os.environ.get("ADMIN_EMAIL")
    password = os.environ.get("ADMIN_PASSWORD")
    if not email or not password:
        print("Set ADMIN_EMAIL and ADMIN_PASSWORD environment variables before running.", file=sys.stderr)
        sys.exit(1)
    if len(password) < 8:
        print("ADMIN_PASSWORD must be at least 8 characters.", file=sys.stderr)
        sys.exit(1)

    prepare_database()
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            user = User(
                full_name=DOCTOR_NAME,
                email=email,
                password_hash=hash_password(password),
                role=UserRole.ADMIN,
                is_active=True,
            )
            db.add(user)
            db.flush()
            print(f"Created admin user: {email}")
        else:
            user.password_hash = hash_password(password)
            user.role = UserRole.ADMIN
            user.full_name = DOCTOR_NAME
            user.is_active = True
            print(f"Updated existing user to admin: {email}")

        if user.doctor_profile is None:
            db.add(
                DoctorProfile(
                    user_id=user.id,
                    specialty="General Veterinary Medicine",
                    years_of_experience=0,
                    verification_status=VerificationStatus.VERIFIED,
                    is_accepting_appointments=True,
                )
            )
            print("Created doctor profile")

        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    main()
