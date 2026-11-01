from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models import EmergencyStatus, Severity
from app.schemas.emergency import (
    EmergencyCreate, EmergencyDetail, EmergencyList, EmergencyOut, StatusUpdate,
)
from app.services import emergency_service as service

router = APIRouter(prefix="/api/emergencies", tags=["Emergencies"])


def _detail(emergency) -> EmergencyDetail:
    detail = EmergencyDetail.model_validate(emergency)
    detail.allowed_next_statuses = service.ALLOWED_TRANSITIONS.get(emergency.status, [])
    return detail


@router.post("", response_model=EmergencyOut, status_code=status.HTTP_201_CREATED)
def create_emergency(data: EmergencyCreate, db: Session = Depends(get_db)):
    """Register a new emergency request (saved in MySQL with status 'pending')."""
    return service.create_emergency(db, data)


@router.get("", response_model=EmergencyList)
def list_emergencies(
    status: Optional[EmergencyStatus] = None,
    severity: Optional[Severity] = None,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    """All emergency requests, newest first. Optional filters: status, severity."""
    total, items = service.list_emergencies(
        db,
        status=status.value if status else None,
        severity=severity.value if severity else None,
        limit=limit,
        offset=offset,
    )
    return {"total": total, "items": items}


@router.get("/{emergency_id}", response_model=EmergencyDetail)
def get_emergency(emergency_id: int, db: Session = Depends(get_db)):
    emergency = service.get_emergency(db, emergency_id)
    if emergency is None:
        raise HTTPException(status_code=404, detail=f"Emergency request {emergency_id} not found")
    return _detail(emergency)


@router.patch("/{emergency_id}/status", response_model=EmergencyDetail)
def update_emergency_status(emergency_id: int, data: StatusUpdate, db: Session = Depends(get_db)):
    emergency = service.get_emergency(db, emergency_id)
    if emergency is None:
        raise HTTPException(status_code=404, detail=f"Emergency request {emergency_id} not found")
    try:
        emergency = service.update_status(db, emergency, data)
    except service.InvalidStatusChange as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    return _detail(emergency)
