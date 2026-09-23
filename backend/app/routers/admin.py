import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import require_staff
from app.models import Appointment, AppointmentStatus, User
from app.schemas import AppointmentAdminOut, AppointmentOut, AppointmentStatusUpdateRequest

router = APIRouter(prefix="/api/admin", tags=["admin"])

# Single-doctor practice: admin endpoints intentionally don't filter by
# doctor_profile_id. If a second doctor is ever added, list/update here
# needs to scope appointments to the current staff user's DoctorProfile.
ALLOWED_TRANSITIONS: dict[AppointmentStatus, set[AppointmentStatus]] = {
    AppointmentStatus.PENDING: {AppointmentStatus.CONFIRMED, AppointmentStatus.COMPLETED, AppointmentStatus.CANCELLED},
    AppointmentStatus.CONFIRMED: {AppointmentStatus.COMPLETED, AppointmentStatus.CANCELLED},
    AppointmentStatus.COMPLETED: set(),
    AppointmentStatus.CANCELLED: set(),
}


def _to_admin_out(appointment: Appointment) -> AppointmentAdminOut:
    return AppointmentAdminOut.model_validate(
        {
            **AppointmentOut.model_validate(appointment).model_dump(),
            "owner_name": appointment.owner.full_name,
            "owner_email": appointment.owner.email,
            "owner_phone": appointment.owner.phone,
        }
    )


@router.get("/appointments", response_model=list[AppointmentAdminOut])
def list_admin_appointments(
    status_filter: AppointmentStatus | None = Query(default=None, alias="status"),
    current_user: User = Depends(require_staff),
    db: Session = Depends(get_db),
) -> list[AppointmentAdminOut]:
    query = db.query(Appointment).order_by(Appointment.scheduled_start.desc())
    if status_filter is not None:
        query = query.filter(Appointment.status == status_filter)
    return [_to_admin_out(appointment) for appointment in query.all()]


@router.patch("/appointments/{appointment_id}/status", response_model=AppointmentAdminOut)
def update_appointment_status(
    appointment_id: uuid.UUID,
    payload: AppointmentStatusUpdateRequest,
    current_user: User = Depends(require_staff),
    db: Session = Depends(get_db),
) -> AppointmentAdminOut:
    appointment = db.get(Appointment, appointment_id)
    if appointment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")

    if payload.cancellation_reason and payload.status != AppointmentStatus.CANCELLED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="cancellation_reason is only valid when cancelling"
        )

    allowed = ALLOWED_TRANSITIONS.get(appointment.status, set())
    if payload.status not in allowed:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Cannot move appointment from {appointment.status.value} to {payload.status.value}",
        )

    now = datetime.now()
    if payload.status == AppointmentStatus.CONFIRMED:
        appointment.confirmed_at = now
    elif payload.status == AppointmentStatus.COMPLETED:
        appointment.completed_at = now
    elif payload.status == AppointmentStatus.CANCELLED:
        appointment.cancelled_at = now
        appointment.cancellation_reason = payload.cancellation_reason
        appointment.cancelled_by_user_id = current_user.id

    appointment.status = payload.status
    db.commit()
    db.refresh(appointment)
    return _to_admin_out(appointment)
