from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel, ConfigDict


class HospitalOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    address: str
    phone: Optional[str]
    latitude: float
    longitude: float
    total_beds: int
    available_beds: int
    has_icu: bool
    has_trauma_centre: bool


class AmbulanceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    registration_number: str
    ambulance_type: str
    status: str
    base_hospital_id: Optional[int]
    base_hospital_name: Optional[str] = None
    current_latitude: Optional[float]
    current_longitude: Optional[float]
    updated_at: datetime


class DashboardSummary(BaseModel):
    total_emergencies: int
    active_emergencies: int
    by_status: Dict[str, int]
    by_severity: Dict[str, int]
    ambulances_total: int
    ambulances_available: int
    hospitals_total: int
