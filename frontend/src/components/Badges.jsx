import {
  AMBULANCE_STATUS_LABELS, SEVERITY_LABELS, STATUS_LABELS, label,
} from "../utils/format.js";

export function SeverityBadge({ value }) {
  return <span className={`badge sev-${value}`}>{label(SEVERITY_LABELS, value)}</span>;
}

export function StatusBadge({ value }) {
  return <span className={`badge st-${value}`}>{label(STATUS_LABELS, value)}</span>;
}

export function AmbulanceStatusBadge({ value }) {
  return <span className={`badge amb-${value}`}>{label(AMBULANCE_STATUS_LABELS, value)}</span>;
}
