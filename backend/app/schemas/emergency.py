"""
Pydantic schemas = the shape of data going IN to and OUT of the API.
FastAPI uses them to validate requests automatically (wrong data -> HTTP 422).
"""
import re
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.database.models import EmergencyStatus, Severity

EMERGENCY_TYPES = ["cardiac", "accident", "breathing", "stroke", "burns", "pregnancy", "other"]
GENDERS = ["male", "female", "other"]
PHONE_PATTERN = re.compile(r"^[0-9+\-\s()]{7,20}$")


class EmergencyCreate(BaseModel):
    caller_name: str = Field(min_length=2, max_length=100)
    caller_phone: str
    patient_name: Optional[str] = Field(default=None, max_length=100)
    patient_age: Optional[int] = Field(default=None, ge=0, le=120)
    patient_gender: Optional[str] = None
    emergency_type: str
    severity: Severity
    description: Optional[str] = Field(default=None, max_length=1000)
    location_address: str = Field(min_length=5, max_length=255)
    latitude: Optional[float] = Field(default=None, ge=-90, le=90)
    longitude: Optional[float] = Field(default=None, ge=-180, le=180)

    @field_validator("caller_name", "location_address")
    @classmethod
    def strip_required_text(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("must not be blank")
        return v

    @field_validator("caller_phone")
    @classmethod
    def check_phone(cls, v: str) -> str:
        v = v.strip()
        if not PHONE_PATTERN.match(v):
            raise ValueError("enter a valid phone number (digits, +, -, spaces; 7 to 20 characters)")
        return v

    @field_validator("emergency_type")
    @classmethod
    def check_type(cls, v: str) -> str:
        v = v.strip().lower()
        if v not in EMERGENCY_TYPES:
            raise ValueError("must be one of: " + ", ".join(EMERGENCY_TYPES))
        return v

    @field_validator("patient_gender")
    @classmethod
    def check_gender(cls, v: Optional[str]) -> Optional[str]:
        if v in (None, ""):
            return None
        v = v.strip().lower()
        if v not in GENDERS:
            raise ValueError("must be one of: " + ", ".join(GENDERS))
        return v

    @model_validator(mode="after")
    def coordinates_together(self):
        if (self.latitude is None) != (self.longitude is None):
            raise ValueError("latitude and longitude must be given together")
        return self


class StatusUpdate(BaseModel):
    status: EmergencyStatus
    remarks: Optional[str] = Field(default=None, max_length=255)


class StatusHistoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    old_status: Optional[str]
    new_status: str
    remarks: Optional[str]
    changed_at: datetime


class EmergencyOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    caller_name: str
    caller_phone: str
    patient_name: Optional[str]
    patient_age: Optional[int]
    patient_gender: Optional[str]
    emergency_type: str
    description: Optional[str]
    severity: str
    status: str
    location_address: str
    latitude: Optional[float]
    longitude: Optional[float]
    created_at: datetime
    updated_at: datetime


class EmergencyDetail(EmergencyOut):
    status_history: List[StatusHistoryOut] = []
    allowed_next_statuses: List[str] = []


class EmergencyList(BaseModel):
    total: int
    items: List[EmergencyOut]
