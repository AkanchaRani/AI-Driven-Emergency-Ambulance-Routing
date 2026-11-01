"""
Sample records for the demonstration.  Everything here is clearly labelled
DEMO / SAMPLE. No real patient, hospital or vehicle information is used.
Seeding only runs on EMPTY tables, so it never duplicates or overwrites data.
"""
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database.models import (
    Ambulance, EmergencyRequest, EmergencyStatusHistory, Hospital, User,
)

# Not a real hash on purpose: login is not part of this build yet.
PLACEHOLDER_HASH = "AUTH_NOT_IMPLEMENTED_YET"


def _is_empty(db: Session, model) -> bool:
    return db.scalar(select(func.count()).select_from(model)) == 0


def seed_sample_data(db: Session) -> list:
    log = []

    if _is_empty(db, User):
        db.add_all([
            User(full_name="Demo Admin", email="admin@demo.local", role="admin", password_hash=PLACEHOLDER_HASH),
            User(full_name="Demo Dispatcher", email="dispatcher@demo.local", role="dispatcher", password_hash=PLACEHOLDER_HASH),
            User(full_name="Demo Driver 1", email="driver1@demo.local", role="driver", password_hash=PLACEHOLDER_HASH),
            User(full_name="Demo Driver 2", email="driver2@demo.local", role="driver", password_hash=PLACEHOLDER_HASH),
        ])
        db.commit()
        log.append("users: 4 sample rows")

    if _is_empty(db, Hospital):
        db.add_all([
            Hospital(name="DEMO City General Hospital", address="Sample Road 1, Demo City", phone="0000000001",
                     latitude=31.3260, longitude=75.5762, total_beds=120, available_beds=34,
                     has_icu=True, has_trauma_centre=True),
            Hospital(name="DEMO Civil Hospital", address="Sample Road 2, Demo City", phone="0000000002",
                     latitude=31.3402, longitude=75.5871, total_beds=80, available_beds=12,
                     has_icu=True, has_trauma_centre=False),
            Hospital(name="DEMO Community Health Centre", address="Sample Road 3, Demo City", phone="0000000003",
                     latitude=31.3105, longitude=75.5599, total_beds=40, available_beds=18,
                     has_icu=False, has_trauma_centre=False),
        ])
        db.commit()
        log.append("hospitals: 3 sample rows")

    if _is_empty(db, Ambulance):
        hospitals = {h.name: h.id for h in db.scalars(select(Hospital)).all()}
        drivers = db.scalars(select(User).where(User.role == "driver").order_by(User.id)).all()
        general = hospitals.get("DEMO City General Hospital")
        civil = hospitals.get("DEMO Civil Hospital")
        db.add_all([
            Ambulance(registration_number="DEMO-AMB-01", ambulance_type="advanced", status="available",
                      driver_id=drivers[0].id if drivers else None, base_hospital_id=general,
                      current_latitude=31.3255, current_longitude=75.5770),
            Ambulance(registration_number="DEMO-AMB-02", ambulance_type="icu", status="available",
                      driver_id=drivers[1].id if len(drivers) > 1 else None, base_hospital_id=general,
                      current_latitude=31.3290, current_longitude=75.5701),
            Ambulance(registration_number="DEMO-AMB-03", ambulance_type="basic", status="dispatched",
                      base_hospital_id=civil, current_latitude=31.3398, current_longitude=75.5880),
            Ambulance(registration_number="DEMO-AMB-04", ambulance_type="basic", status="maintenance",
                      base_hospital_id=civil, current_latitude=31.3402, current_longitude=75.5871),
        ])
        db.commit()
        log.append("ambulances: 4 sample rows")

    if _is_empty(db, EmergencyRequest):
        samples = [
            ("Demo Caller A", "9000000001", "Demo Patient A", 58, "male", "cardiac", "critical",
             "Sample record: chest pain and sweating.", "Sample Chowk, Demo City", "assigned"),
            ("Demo Caller B", "9000000002", "Demo Patient B", 27, "female", "accident", "high",
             "Sample record: two-wheeler collision, leg injury.", "Sample Bypass Road, Demo City", "pending"),
            ("Demo Caller C", "9000000003", "Demo Patient C", 72, "male", "breathing", "medium",
             "Sample record: breathlessness at home.", "Sample Colony, Demo City", "completed"),
        ]
        for caller, phone, patient, age, gender, etype, sev, desc, addr, status in samples:
            e = EmergencyRequest(
                caller_name=caller, caller_phone=phone, patient_name=patient, patient_age=age,
                patient_gender=gender, emergency_type=etype, severity=sev, description=desc,
                location_address=addr, status=status,
            )
            db.add(e)
            db.flush()
            db.add(EmergencyStatusHistory(emergency_id=e.id, old_status=None, new_status="pending",
                                          remarks="Sample record created by seed script"))
            if status != "pending":
                db.add(EmergencyStatusHistory(emergency_id=e.id, old_status="pending", new_status=status,
                                              remarks="Sample status set by seed script"))
        db.commit()
        log.append("emergency_requests: 3 sample rows")

    return log or ["nothing to seed (tables already have data)"]
