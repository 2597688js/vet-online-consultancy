from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import (
    Appointment,
    AppointmentStatus,
    ConsultationType,
    DoctorProfile,
    Pet,
    User,
    VerificationStatus,
)
from app.schemas import AppointmentCreateRequest, AppointmentOut

router = APIRouter(prefix="/api/appointments", tags=["appointments"])

DEFAULT_DURATION_MINUTES = 30
DEFAULT_CONSULTATION_TYPE = ConsultationType.VIDEO


def get_solo_doctor(db: Session) -> DoctorProfile:
    doctor = (
        db.query(DoctorProfile)
        .filter(
            DoctorProfile.verification_status == VerificationStatus.VERIFIED,
            DoctorProfile.is_accepting_appointments.is_(True),
        )
        .order_by(DoctorProfile.created_at.asc())
        .first()
    )
    if doctor is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Booking is not available right now"
        )
    return doctor


@router.post("", response_model=AppointmentOut, status_code=status.HTTP_201_CREATED)
def create_appointment(
    payload: AppointmentCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Appointment:
    pet = db.get(Pet, payload.pet_id)
    if pet is None or pet.deleted_at is not None or pet.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found")

    doctor = get_solo_doctor(db)

    # No time is chosen at booking; Dr. Sarkar contacts the owner to arrange the consultation.
    appointment = Appointment(
        pet_id=pet.id,
        owner_id=current_user.id,
        doctor_profile_id=doctor.id,
        consultation_type=DEFAULT_CONSULTATION_TYPE,
        duration_minutes=DEFAULT_DURATION_MINUTES,
        price_at_booking=Decimal("0.00"),
        currency="INR",
        symptoms=payload.symptoms.strip(),
        contact_name=payload.contact_name.strip(),
        contact_phone=payload.contact_phone.strip(),
        status=AppointmentStatus.PENDING,
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment
