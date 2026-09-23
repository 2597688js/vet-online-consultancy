import enum
import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    Date,
    DateTime,
    ForeignKey,
    Index,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import ARRAY, ENUM as PgEnum, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def gen_uuid() -> uuid.UUID:
    return uuid.uuid4()


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class UserRole(str, enum.Enum):
    OWNER = "OWNER"
    VET = "VET"
    ADMIN = "ADMIN"


class PetGender(str, enum.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    UNKNOWN = "UNKNOWN"


class ConsultationType(str, enum.Enum):
    VIDEO = "VIDEO"
    AUDIO = "AUDIO"
    CHAT = "CHAT"


class VerificationStatus(str, enum.Enum):
    PENDING = "PENDING"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"
    SUSPENDED = "SUSPENDED"


class AppointmentStatus(str, enum.Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


def pg_enum(python_enum: type[enum.Enum], name: str) -> PgEnum:
    return PgEnum(python_enum, name=name, values_callable=lambda e: [item.value for item in e])


# ---------------------------------------------------------------------------
# User (single table, role-discriminated)
# ---------------------------------------------------------------------------


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=gen_uuid)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    password_hash: Mapped[str | None] = mapped_column(String, nullable=True)
    google_id: Mapped[str | None] = mapped_column(String, unique=True, nullable=True)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    phone: Mapped[str | None] = mapped_column(String, unique=True, nullable=True)
    role: Mapped[UserRole] = mapped_column(pg_enum(UserRole, "user_role"), default=UserRole.OWNER, index=True, nullable=False)
    avatar_url: Mapped[str | None] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    email_verified_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    pets: Mapped[list["Pet"]] = relationship(back_populates="owner", foreign_keys="Pet.owner_id")
    doctor_profile: Mapped["DoctorProfile | None"] = relationship(
        back_populates="user", foreign_keys="DoctorProfile.user_id", uselist=False
    )


# ---------------------------------------------------------------------------
# Pet
# ---------------------------------------------------------------------------


class Pet(Base):
    __tablename__ = "pets"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=gen_uuid)
    owner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), index=True, nullable=False)
    name: Mapped[str | None] = mapped_column(String, nullable=True)
    species: Mapped[str] = mapped_column(String, index=True, nullable=False)
    breed: Mapped[str | None] = mapped_column(String, nullable=True)
    gender: Mapped[PetGender] = mapped_column(pg_enum(PetGender, "pet_gender"), default=PetGender.UNKNOWN, nullable=False)
    date_of_birth: Mapped[date | None] = mapped_column(Date, nullable=True)
    weight_kg: Mapped[Decimal | None] = mapped_column(Numeric(6, 2), nullable=True)
    color: Mapped[str | None] = mapped_column(String, nullable=True)
    allergies: Mapped[str | None] = mapped_column(Text, nullable=True)
    existing_conditions: Mapped[str | None] = mapped_column(Text, nullable=True)
    current_medications: Mapped[str | None] = mapped_column(Text, nullable=True)
    medical_history: Mapped[str | None] = mapped_column(Text, nullable=True)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    owner: Mapped["User"] = relationship(back_populates="pets", foreign_keys=[owner_id])
    appointments: Mapped[list["Appointment"]] = relationship(back_populates="pet", foreign_keys="Appointment.pet_id")


# ---------------------------------------------------------------------------
# DoctorProfile (1:1 with User where role = VET)
# ---------------------------------------------------------------------------


class DoctorProfile(Base):
    __tablename__ = "doctor_profiles"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=gen_uuid)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    specialty: Mapped[str] = mapped_column(String, index=True, nullable=False)
    specializations: Mapped[list[str]] = mapped_column(ARRAY(String), default=list, nullable=False)
    license_number: Mapped[str | None] = mapped_column(String, unique=True, nullable=True)
    years_of_experience: Mapped[int] = mapped_column(default=0, nullable=False)
    education: Mapped[str | None] = mapped_column(Text, nullable=True)
    languages: Mapped[list[str]] = mapped_column(ARRAY(String), default=list, nullable=False)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    rating: Mapped[Decimal] = mapped_column(Numeric(3, 2), default=0, nullable=False)
    rating_count: Mapped[int] = mapped_column(default=0, nullable=False)
    verification_status: Mapped[VerificationStatus] = mapped_column(
        pg_enum(VerificationStatus, "verification_status"), default=VerificationStatus.PENDING, index=True, nullable=False
    )
    verified_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    verified_by_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    is_accepting_appointments: Mapped[bool] = mapped_column(default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    user: Mapped["User"] = relationship(back_populates="doctor_profile", foreign_keys=[user_id])
    verified_by: Mapped["User | None"] = relationship(foreign_keys=[verified_by_id])


# ---------------------------------------------------------------------------
# Appointment — consultation request linking pet + doctor + consultation type
# ---------------------------------------------------------------------------


class Appointment(Base):
    __tablename__ = "appointments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=gen_uuid)
    pet_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("pets.id", ondelete="RESTRICT"), nullable=False)
    owner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    doctor_profile_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("doctor_profiles.id", ondelete="RESTRICT"), nullable=False
    )

    consultation_type: Mapped[ConsultationType] = mapped_column(pg_enum(ConsultationType, "consultation_type"), nullable=False)
    duration_minutes: Mapped[int] = mapped_column(nullable=False)
    price_at_booking: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String, default="USD", nullable=False)

    # Owners no longer pick a time; the doctor contacts them. Kept for bookings made with a slot.
    scheduled_start: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    scheduled_end: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    symptoms: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Contact details given on the booking form; may differ from the account's name/phone.
    contact_name: Mapped[str | None] = mapped_column(String, nullable=True)
    contact_phone: Mapped[str | None] = mapped_column(String, nullable=True)
    home_visit_required: Mapped[bool] = mapped_column(default=False, server_default="false", nullable=False)
    home_visit_address: Mapped[str | None] = mapped_column(Text, nullable=True)

    status: Mapped[AppointmentStatus] = mapped_column(
        pg_enum(AppointmentStatus, "appointment_status"), default=AppointmentStatus.PENDING, index=True, nullable=False
    )
    confirmed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    cancelled_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    cancellation_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    cancelled_by_user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    reminder_sent_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    pet: Mapped["Pet"] = relationship(back_populates="appointments", foreign_keys=[pet_id])
    owner: Mapped["User"] = relationship(foreign_keys=[owner_id])
    doctor_profile: Mapped["DoctorProfile"] = relationship()
    cancelled_by: Mapped["User | None"] = relationship(foreign_keys=[cancelled_by_user_id])


# extra composite indexes (declared separately to keep single-column ones above readable)
Index("ix_appointments_owner_status", Appointment.owner_id, Appointment.status)
Index("ix_appointments_doctor_scheduled_start", Appointment.doctor_profile_id, Appointment.scheduled_start)
Index("ix_appointments_scheduled_start", Appointment.scheduled_start)

