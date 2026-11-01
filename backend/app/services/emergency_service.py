"""
Business logic for emergency requests.
Routers call these functions; these functions talk to the database.
Keeping them separate means the AI / routing modules can reuse them later.
"""
from typing import List, Optional, Tuple

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.database.models import (
    EmergencyRequest, EmergencyStatus, EmergencyStatusHistory, Notification, User,
)
from app.schemas.emergency import EmergencyCreate, StatusUpdate

# Which status can follow which. Completed and cancelled are final.
ALLOWED_TRANSITIONS = {
    "pending": ["assigned", "cancelled"],
    "assigned": ["en_route", "cancelled"],
    "en_route": ["at_scene", "cancelled"],
    "at_scene": ["transporting", "cancelled"],
    "transporting": ["completed"],
    "completed": [],
    "cancelled": [],
}


class InvalidStatusChange(Exception):
    pass


def create_emergency(db: Session, data: EmergencyCreate) -> EmergencyRequest:
    emergency = EmergencyRequest(
        **data.model_dump(exclude={"severity"}),
        severity=data.severity.value,
        status=EmergencyStatus.pending.value,
    )
    db.add(emergency)
    db.flush()  # gives us emergency.id without committing yet

    db.add(EmergencyStatusHistory(
        emergency_id=emergency.id,
        old_status=None,
        new_status=EmergencyStatus.pending.value,
        remarks="Request registered",
    ))

    # Tell every active dispatcher/admin about the new request
    staff = db.scalars(
        select(User).where(User.is_active.is_(True), User.role.in_(["admin", "dispatcher"]))
    ).all()
    for user in staff:
        db.add(Notification(
            user_id=user.id,
            emergency_id=emergency.id,
            title=f"New {emergency.severity} emergency",
            message=f"Request #{emergency.id}: {emergency.emergency_type} at {emergency.location_address}",
        ))

    db.commit()
    db.refresh(emergency)
    return emergency


def list_emergencies(
    db: Session,
    status: Optional[str] = None,
    severity: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
) -> Tuple[int, List[EmergencyRequest]]:
    query = select(EmergencyRequest)
    count_query = select(func.count()).select_from(EmergencyRequest)
    if status:
        query = query.where(EmergencyRequest.status == status)
        count_query = count_query.where(EmergencyRequest.status == status)
    if severity:
        query = query.where(EmergencyRequest.severity == severity)
        count_query = count_query.where(EmergencyRequest.severity == severity)

    total = db.scalar(count_query)
    items = db.scalars(
        query.order_by(EmergencyRequest.created_at.desc(), EmergencyRequest.id.desc())
        .limit(limit).offset(offset)
    ).all()
    return total, items


def get_emergency(db: Session, emergency_id: int) -> Optional[EmergencyRequest]:
    return db.scalar(
        select(EmergencyRequest)
        .options(selectinload(EmergencyRequest.status_history))
        .where(EmergencyRequest.id == emergency_id)
    )


def update_status(db: Session, emergency: EmergencyRequest, data: StatusUpdate) -> EmergencyRequest:
    new_status = data.status.value
    allowed = ALLOWED_TRANSITIONS.get(emergency.status, [])
    if new_status not in allowed:
        if allowed:
            hint = "Allowed next status: " + ", ".join(allowed)
        else:
            hint = "This request is already closed"
        raise InvalidStatusChange(
            f"Cannot change status from '{emergency.status}' to '{new_status}'. {hint}."
        )

    db.add(EmergencyStatusHistory(
        emergency_id=emergency.id,
        old_status=emergency.status,
        new_status=new_status,
        remarks=data.remarks,
    ))
    emergency.status = new_status
    db.commit()
    return get_emergency(db, emergency.id)
