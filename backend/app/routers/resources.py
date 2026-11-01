"""Read-only endpoints for hospitals, ambulances and dashboard numbers."""
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.database.connection import get_db
from app.database.models import Ambulance, Hospital
from app.schemas.resources import AmbulanceOut, DashboardSummary, HospitalOut
from app.services import dashboard_service

router = APIRouter(prefix="/api", tags=["Resources"])


@router.get("/hospitals", response_model=List[HospitalOut])
def list_hospitals(db: Session = Depends(get_db)):
    return db.scalars(select(Hospital).order_by(Hospital.name)).all()


@router.get("/ambulances", response_model=List[AmbulanceOut])
def list_ambulances(db: Session = Depends(get_db)):
    ambulances = db.scalars(
        select(Ambulance).options(joinedload(Ambulance.base_hospital)).order_by(Ambulance.registration_number)
    ).all()
    result = []
    for amb in ambulances:
        item = AmbulanceOut.model_validate(amb)
        item.base_hospital_name = amb.base_hospital.name if amb.base_hospital else None
        result.append(item)
    return result


@router.get("/dashboard/summary", response_model=DashboardSummary)
def dashboard_summary(db: Session = Depends(get_db)):
    return dashboard_service.get_summary(db)
