import uuid
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, EmailStr, Field

from app.models import AppointmentStatus, ConsultationType, PetGender, UserRole


class RegisterRequest(BaseModel):
    full_name: str = Field(min_length=1, max_length=200)
    email: EmailStr
    phone: str = Field(min_length=7, max_length=30)
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: uuid.UUID
    full_name: str
    email: EmailStr
    phone: str | None
    role: UserRole
    created_at: datetime

    model_config = {"from_attributes": True}


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class GoogleAuthRequest(BaseModel):
    credential: str


# ---------------------------------------------------------------------------
# Pets
# ---------------------------------------------------------------------------


class PetCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    species: str = Field(min_length=1, max_length=100)
    breed: str | None = Field(default=None, max_length=100)
    gender: PetGender = PetGender.UNKNOWN
    date_of_birth: date | None = None
    weight_kg: Decimal | None = None
    color: str | None = Field(default=None, max_length=100)
    allergies: str | None = None
    existing_conditions: str | None = None
    current_medications: str | None = None


class PetPhotoOut(BaseModel):
    id: uuid.UUID
    url: str
    created_at: datetime

    model_config = {"from_attributes": True}


class PetOut(BaseModel):
    id: uuid.UUID
    name: str
    species: str
    breed: str | None
    gender: PetGender
    date_of_birth: date | None
    weight_kg: Decimal | None
    color: str | None
    allergies: str | None
    existing_conditions: str | None
    current_medications: str | None
    photos: list[PetPhotoOut]
    created_at: datetime

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Appointments
# ---------------------------------------------------------------------------


class SlotOut(BaseModel):
    start: datetime
    end: datetime
    available: bool


class AppointmentCreateRequest(BaseModel):
    pet_id: uuid.UUID
    scheduled_start: datetime
    symptoms: str | None = None


class AppointmentOut(BaseModel):
    id: uuid.UUID
    pet: PetOut
    consultation_type: ConsultationType
    duration_minutes: int
    price_at_booking: Decimal
    currency: str
    scheduled_start: datetime
    scheduled_end: datetime
    symptoms: str | None
    status: AppointmentStatus
    confirmed_at: datetime | None
    cancellation_reason: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class AppointmentAdminOut(AppointmentOut):
    owner_name: str
    owner_email: EmailStr
    owner_phone: str | None


class AppointmentStatusUpdateRequest(BaseModel):
    status: AppointmentStatus
    cancellation_reason: str | None = Field(default=None, max_length=1000)
