from datetime import date, datetime, timedelta
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
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
from app.schemas import AppointmentCreateRequest, AppointmentOut, SlotOut

router = APIRouter(prefix="/api/appointments", tags=["appointments"])

SLOT_DURATION_MINUTES = 30
BOOKING_WINDOW_START_MINUTES = 12 * 60  # 12:00 noon
BOOKING_WINDOW_END_MINUTES = 21 * 60  # 9:00 pm
DEFAULT_CONSULTATION_TYPE = ConsultationType.VIDEO
BOOKING_HORIZON_DAYS = 30

ACTIVE_STATUSES = (AppointmentStatus.PENDING, AppointmentStatus.CONFIRMED)


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


def _slot_starts_for_day(day: date) -> list[datetime]:
    starts = []
    minutes = BOOKING_WINDOW_START_MINUTES
    while minutes + SLOT_DURATION_MINUTES <= BOOKING_WINDOW_END_MINUTES:
        starts.append(datetime.combine(day, datetime.min.time()) + timedelta(minutes=minutes))
        minutes += SLOT_DURATION_MINUTES
    return starts


def _is_valid_slot_start(dt: datetime) -> bool:
    return dt in _slot_starts_for_day(dt.date())


@router.get("/slots", response_model=list[SlotOut])
def get_slots(booking_date: date, db: Session = Depends(get_db)) -> list[SlotOut]:
    today = datetime.now().date()
    if booking_date < today or booking_date > today + timedelta(days=BOOKING_HORIZON_DAYS):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Date is outside the booking window")

    doctor = get_solo_doctor(db)

    day_start = datetime.combine(booking_date, datetime.min.time())
    day_end = day_start + timedelta(days=1)
    taken = {
        row.scheduled_start
        for row in db.query(Appointment.scheduled_start).filter(
            Appointment.doctor_profile_id == doctor.id,
            Appointment.status.in_(ACTIVE_STATUSES),
            Appointment.scheduled_start >= day_start,
            Appointment.scheduled_start < day_end,
        )
    }

    now = datetime.now()
    slots = []
    for start in _slot_starts_for_day(booking_date):
        slots.append(
            SlotOut(
                start=start,
                end=start + timedelta(minutes=SLOT_DURATION_MINUTES),
                available=start not in taken and start > now,
            )
        )
    return slots


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

    scheduled_start = payload.scheduled_start.replace(tzinfo=None)
    if scheduled_start <= datetime.now():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Slot is in the past")
    if not _is_valid_slot_start(scheduled_start):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not a valid appointment slot")

    offering = (
        db.query(ConsultationOffering)
        .filter(
            ConsultationOffering.doctor_profile_id == doctor.id,
            ConsultationOffering.type == DEFAULT_CONSULTATION_TYPE,
            ConsultationOffering.is_active.is_(True),
        )
        .first()
    )

    appointment = Appointment(
        pet_id=pet.id,
        owner_id=current_user.id,
        doctor_profile_id=doctor.id,
        consultation_offering_id=offering.id if offering else None,
        consultation_type=DEFAULT_CONSULTATION_TYPE,
        duration_minutes=offering.duration_minutes if offering else SLOT_DURATION_MINUTES,
        price_at_booking=offering.price if offering else Decimal("0.00"),
        currency=offering.currency if offering else "INR",
        scheduled_start=scheduled_start,
        scheduled_end=scheduled_start + timedelta(minutes=SLOT_DURATION_MINUTES),
        symptoms=payload.symptoms,
        status=AppointmentStatus.PENDING,
    )
    db.add(appointment)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="That slot was just booked. Please choose another.")
    db.refresh(appointment)
    return appointment


@router.get("/me", response_model=list[AppointmentOut])
def list_my_appointments(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[Appointment]:
    return (
        db.query(Appointment)
        .filter(Appointment.owner_id == current_user.id)
        .order_by(Appointment.scheduled_start.desc())
        .all()
    )
