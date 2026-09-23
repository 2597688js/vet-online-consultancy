import uuid
from datetime import date, datetime
from io import BytesIO

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from openpyxl import Workbook
from openpyxl.styles import Font
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Appointment, AppointmentStatus, PetGender, User, UserRole
from app.schemas import AppointmentAdminOut, AppointmentOut, AppointmentStatusUpdateRequest

router = APIRouter(prefix="/api/admin", tags=["admin"])

# Single-doctor practice. There's no admin login: the dashboard and these endpoints are open by design.
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
            "owner_name": appointment.contact_name or appointment.owner.full_name,
            "owner_email": appointment.owner.email,
            "owner_phone": appointment.contact_phone or appointment.owner.phone,
        }
    )


@router.get("/appointments", response_model=list[AppointmentAdminOut])
def list_admin_appointments(
    status_filter: AppointmentStatus | None = Query(default=None, alias="status"),
    db: Session = Depends(get_db),
) -> list[AppointmentAdminOut]:
    query = db.query(Appointment).order_by(Appointment.created_at.desc())
    if status_filter is not None:
        query = query.filter(Appointment.status == status_filter)
    return [_to_admin_out(appointment) for appointment in query.all()]


SEX_LABELS = {PetGender.MALE: "Male", PetGender.FEMALE: "Female", PetGender.UNKNOWN: "Not sure"}


def _age(date_of_birth: date | None) -> str:
    if date_of_birth is None:
        return ""
    today = date.today()
    months = (today.year - date_of_birth.year) * 12 + today.month - date_of_birth.month
    if today.day < date_of_birth.day:
        months -= 1
    years, months = divmod(max(months, 0), 12)
    return f"{years} yrs {months} mo"


def _format_datetime(value: datetime | None) -> str:
    return value.strftime("%Y-%m-%d %H:%M") if value else ""


# (column header, value getter) for the Excel export: one row per request, owner and pet details included.
EXPORT_COLUMNS = [
    ("Submitted", lambda a: _format_datetime(a.created_at)),
    ("Status", lambda a: a.status.value.title()),
    ("Home visit required", lambda a: "Yes" if a.home_visit_required else "No"),
    ("Home visit address", lambda a: a.home_visit_address or ""),
    ("Owner name", lambda a: a.contact_name or a.owner.full_name),
    ("Owner WhatsApp", lambda a: a.contact_phone or a.owner.phone or ""),
    ("Account name", lambda a: a.owner.full_name),
    ("Account email", lambda a: a.owner.email),
    ("Account phone", lambda a: a.owner.phone or ""),
    ("Pet name", lambda a: a.pet.name or ""),
    ("Species", lambda a: a.pet.species),
    ("Breed", lambda a: a.pet.breed or ""),
    ("Sex", lambda a: SEX_LABELS[a.pet.gender]),
    ("Age", lambda a: _age(a.pet.date_of_birth)),
    ("Date of birth (approx.)", lambda a: a.pet.date_of_birth.isoformat() if a.pet.date_of_birth else ""),
    ("Weight (kg)", lambda a: float(a.pet.weight_kg) if a.pet.weight_kg is not None else ""),
    ("Color / markings", lambda a: a.pet.color or ""),
    ("Main problem", lambda a: a.symptoms or ""),
    ("Medical history", lambda a: a.pet.medical_history or a.pet.existing_conditions or ""),
    ("Current medications", lambda a: a.pet.current_medications or ""),
    ("Allergies", lambda a: a.pet.allergies or ""),
    ("Scheduled time", lambda a: _format_datetime(a.scheduled_start)),
    ("Confirmed", lambda a: _format_datetime(a.confirmed_at)),
    ("Completed", lambda a: _format_datetime(a.completed_at)),
    ("Cancelled", lambda a: _format_datetime(a.cancelled_at)),
    ("Cancellation reason", lambda a: a.cancellation_reason or ""),
]


@router.get("/appointments/export")
def export_appointments(db: Session = Depends(get_db)) -> Response:
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Consultation requests"
    sheet.append([header for header, _ in EXPORT_COLUMNS])
    for cell in sheet[1]:
        cell.font = Font(bold=True)
    sheet.freeze_panes = "A2"

    for appointment in db.query(Appointment).order_by(Appointment.created_at.desc()).all():
        sheet.append([getter(appointment) for _, getter in EXPORT_COLUMNS])

    for column in sheet.columns:
        longest = max(len(str(cell.value or "")) for cell in column)
        sheet.column_dimensions[column[0].column_letter].width = min(max(longest + 2, 12), 50)

    buffer = BytesIO()
    workbook.save(buffer)
    filename = f"consultation-requests-{date.today().isoformat()}.xlsx"
    return Response(
        content=buffer.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


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
        doctor = db.query(User).filter(User.role == UserRole.ADMIN).order_by(User.created_at.asc()).first()
        appointment.cancelled_by_user_id = doctor.id if doctor else None

    appointment.status = payload.status
    db.commit()
    db.refresh(appointment)
    return _to_admin_out(appointment)
