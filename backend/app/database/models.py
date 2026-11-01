"""
SQLAlchemy models = Python classes that map to MySQL tables.

Tables (8):
  users, hospitals, ambulances, emergency_requests,
  assignments, routes, notifications, emergency_status_history

Note on status/severity columns: they are stored as short text (VARCHAR) and
the allowed values are listed in the Enum classes below. We did this so that
adding a new status later is a code change, not a risky ALTER TABLE.
"""
import enum
from datetime import datetime, timezone

from sqlalchemy import (
    Boolean, Column, DateTime, Float, ForeignKey, Index, Integer, Numeric,
    String, Text,
)
from sqlalchemy.orm import relationship

from app.database.connection import Base


def utc_now():
    """Current UTC time (naive) - used as default for created_at / updated_at."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


# ----------------------------------------------------------------- allowed values
class UserRole(str, enum.Enum):
    admin = "admin"
    dispatcher = "dispatcher"
    driver = "driver"
    hospital_staff = "hospital_staff"


class Severity(str, enum.Enum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"


class EmergencyStatus(str, enum.Enum):
    pending = "pending"
    assigned = "assigned"
    en_route = "en_route"
    at_scene = "at_scene"
    transporting = "transporting"
    completed = "completed"
    cancelled = "cancelled"


class AmbulanceStatus(str, enum.Enum):
    available = "available"
    dispatched = "dispatched"
    maintenance = "maintenance"
    offline = "offline"


class AmbulanceType(str, enum.Enum):
    basic = "basic"        # BLS
    advanced = "advanced"  # ALS
    icu = "icu"            # mobile ICU


class RouteType(str, enum.Enum):
    to_scene = "to_scene"
    to_hospital = "to_hospital"


# ----------------------------------------------------------------- tables
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(120), nullable=False, unique=True)
    phone = Column(String(20))
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default=UserRole.dispatcher.value)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=utc_now)
    updated_at = Column(DateTime, nullable=False, default=utc_now, onupdate=utc_now)

    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")


class Hospital(Base):
    __tablename__ = "hospitals"

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False, unique=True)
    address = Column(String(255), nullable=False)
    phone = Column(String(20))
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    total_beds = Column(Integer, nullable=False, default=0)
    # Entered by hand for now. Not verified against a real hospital system.
    available_beds = Column(Integer, nullable=False, default=0)
    has_icu = Column(Boolean, nullable=False, default=False)
    has_trauma_centre = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=utc_now)
    updated_at = Column(DateTime, nullable=False, default=utc_now, onupdate=utc_now)

    ambulances = relationship("Ambulance", back_populates="base_hospital")
    assignments = relationship("Assignment", back_populates="hospital")


class Ambulance(Base):
    __tablename__ = "ambulances"

    id = Column(Integer, primary_key=True)
    registration_number = Column(String(30), nullable=False, unique=True)
    ambulance_type = Column(String(20), nullable=False, default=AmbulanceType.basic.value)
    status = Column(String(20), nullable=False, default=AmbulanceStatus.available.value)
    driver_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    base_hospital_id = Column(Integer, ForeignKey("hospitals.id", ondelete="SET NULL"))
    # Last known position, entered by hand. Live GPS tracking is a future module.
    current_latitude = Column(Float)
    current_longitude = Column(Float)
    created_at = Column(DateTime, nullable=False, default=utc_now)
    updated_at = Column(DateTime, nullable=False, default=utc_now, onupdate=utc_now)

    driver = relationship("User")
    base_hospital = relationship("Hospital", back_populates="ambulances")
    assignments = relationship("Assignment", back_populates="ambulance")

    __table_args__ = (Index("ix_ambulances_status", "status"),)


class EmergencyRequest(Base):
    __tablename__ = "emergency_requests"

    id = Column(Integer, primary_key=True)
    caller_name = Column(String(100), nullable=False)
    caller_phone = Column(String(20), nullable=False)
    patient_name = Column(String(100))
    patient_age = Column(Integer)
    patient_gender = Column(String(10))
    emergency_type = Column(String(30), nullable=False)
    description = Column(Text)
    # Chosen by the person entering the request. ML classification is pending.
    severity = Column(String(10), nullable=False)
    status = Column(String(20), nullable=False, default=EmergencyStatus.pending.value)
    location_address = Column(String(255), nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    created_at = Column(DateTime, nullable=False, default=utc_now)
    updated_at = Column(DateTime, nullable=False, default=utc_now, onupdate=utc_now)

    assignments = relationship("Assignment", back_populates="emergency", cascade="all, delete-orphan")
    status_history = relationship(
        "EmergencyStatusHistory",
        back_populates="emergency",
        cascade="all, delete-orphan",
        order_by="EmergencyStatusHistory.changed_at",
    )

    __table_args__ = (
        Index("ix_emergency_status", "status"),
        Index("ix_emergency_severity", "severity"),
        Index("ix_emergency_created_at", "created_at"),
    )


class Assignment(Base):
    """Which ambulance (and destination hospital) was given to which emergency."""
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True)
    emergency_id = Column(Integer, ForeignKey("emergency_requests.id", ondelete="CASCADE"), nullable=False)
    ambulance_id = Column(Integer, ForeignKey("ambulances.id", ondelete="RESTRICT"), nullable=False)
    hospital_id = Column(Integer, ForeignKey("hospitals.id", ondelete="SET NULL"))
    assigned_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    status = Column(String(20), nullable=False, default="active")
    notes = Column(String(255))
    assigned_at = Column(DateTime, nullable=False, default=utc_now)
    updated_at = Column(DateTime, nullable=False, default=utc_now, onupdate=utc_now)

    emergency = relationship("EmergencyRequest", back_populates="assignments")
    ambulance = relationship("Ambulance", back_populates="assignments")
    hospital = relationship("Hospital", back_populates="assignments")
    routes = relationship("Route", back_populates="assignment", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_assignments_emergency", "emergency_id"),
        Index("ix_assignments_ambulance", "ambulance_id"),
    )


class Route(Base):
    """Route for an assignment. Filled by the OSM/OSRM module later."""
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id", ondelete="CASCADE"), nullable=False)
    route_type = Column(String(20), nullable=False, default=RouteType.to_scene.value)
    distance_km = Column(Numeric(8, 2))
    estimated_minutes = Column(Numeric(6, 1))
    geometry = Column(Text)  # encoded polyline / GeoJSON from OSRM
    source = Column(String(30), nullable=False, default="manual")
    created_at = Column(DateTime, nullable=False, default=utc_now)

    assignment = relationship("Assignment", back_populates="routes")

    __table_args__ = (Index("ix_routes_assignment", "assignment_id"),)


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    emergency_id = Column(Integer, ForeignKey("emergency_requests.id", ondelete="CASCADE"))
    title = Column(String(150), nullable=False)
    message = Column(String(500), nullable=False)
    is_read = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=utc_now)

    user = relationship("User", back_populates="notifications")

    __table_args__ = (Index("ix_notifications_user_read", "user_id", "is_read"),)


class EmergencyStatusHistory(Base):
    """One row every time an emergency changes status (audit trail)."""
    __tablename__ = "emergency_status_history"

    id = Column(Integer, primary_key=True)
    emergency_id = Column(Integer, ForeignKey("emergency_requests.id", ondelete="CASCADE"), nullable=False)
    old_status = Column(String(20))
    new_status = Column(String(20), nullable=False)
    changed_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    remarks = Column(String(255))
    changed_at = Column(DateTime, nullable=False, default=utc_now)

    emergency = relationship("EmergencyRequest", back_populates="status_history")

    __table_args__ = (Index("ix_status_history_emergency", "emergency_id"),)
