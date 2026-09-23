from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import (
    Appointment,
    AppointmentStatus,
    ConsultationOffering,
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

    offering = (
        db.query(ConsultationOffering)
        .filter(
            ConsultationOffering.doctor_profile_id == doctor.id,
            ConsultationOffering.type == DEFAULT_CONSULTATION_TYPE,
            ConsultationOffering.is_active.is_(True),
        )
        .first()
    )

    # No time is chosen at booking; Dr. Sarkar contacts the owner to arrange the consultation.
    appointment = Appointment(
        pet_id=pet.id,
        owner_id=current_user.id,
        doctor_profile_id=doctor.id,
        consultation_offering_id=offering.id if offering else None,
        consultation_type=DEFAULT_CONSULTATION_TYPE,
        duration_minutes=offering.duration_minutes if offering else DEFAULT_DURATION_MINUTES,
        price_at_booking=offering.price if offering else Decimal("0.00"),
        currency=offering.currency if offering else "INR",
        symptoms=payload.symptoms.strip(),
        contact_name=payload.contact_name.strip(),
        contact_phone=payload.contact_phone.strip(),
        status=AppointmentStatus.PENDING,
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment


@router.get("/me", response_model=list[AppointmentOut])
def list_my_appointments(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[Appointment]:
    return (
        db.query(Appointment)
        .filter(Appointment.owner_id == current_user.id)
        .order_by(Appointment.created_at.desc())
        .all()
    )
