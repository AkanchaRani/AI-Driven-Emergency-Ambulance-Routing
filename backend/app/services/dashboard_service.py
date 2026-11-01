"""Counts for the dashboard. Every number comes from a real SQL query."""
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database.models import Ambulance, EmergencyRequest, Hospital


def _group_counts(db: Session, column) -> dict:
    rows = db.execute(select(column, func.count()).group_by(column)).all()
    return {value: count for value, count in rows}


def get_summary(db: Session) -> dict:
    by_status = _group_counts(db, EmergencyRequest.status)
    by_severity = _group_counts(db, EmergencyRequest.severity)
    closed = by_status.get("completed", 0) + by_status.get("cancelled", 0)
    total = sum(by_status.values())

    return {
        "total_emergencies": total,
        "active_emergencies": total - closed,
        "by_status": by_status,
        "by_severity": by_severity,
        "ambulances_total": db.scalar(select(func.count()).select_from(Ambulance)),
        "ambulances_available": db.scalar(
            select(func.count()).select_from(Ambulance).where(Ambulance.status == "available")
        ),
        "hospitals_total": db.scalar(select(func.count()).select_from(Hospital)),
    }
