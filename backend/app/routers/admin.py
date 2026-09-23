import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Appointment, AppointmentStatus
from app.routers.appointments import get_solo_doctor
from app.schemas import AppointmentAdminOut, AppointmentOut, AppointmentStatusUpdateRequest

router = APIRouter(prefix="/api/admin", tags=["admin"])

# Single-doctor practice: admin endpoints intentionally don't filter by
# doctor_profile_id. There's no admin login: the dashboard and these endpoints are open by design.
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
        appointment.cancelled_by_user_id = get_solo_doctor(db).user_id

    appointment.status = payload.status
    db.commit()
    db.refresh(appointment)
    return _to_admin_out(appointment)
