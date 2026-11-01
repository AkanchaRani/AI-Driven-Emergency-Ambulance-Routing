export const STATUS_LABELS = {
  pending: "Pending",
  assigned: "Assigned",
  en_route: "En route",
  at_scene: "At scene",
  transporting: "Transporting",
  completed: "Completed",
  cancelled: "Cancelled",
};

export const SEVERITY_LABELS = {
  critical: "Critical",
  high: "High",
  medium: "Medium",
  low: "Low",
};

export const TYPE_LABELS = {
  cardiac: "Cardiac",
  accident: "Road accident",
  breathing: "Breathing problem",
  stroke: "Stroke",
  burns: "Burns",
  pregnancy: "Pregnancy",
  other: "Other",
};

export const AMBULANCE_STATUS_LABELS = {
  available: "Available",
  dispatched: "Dispatched",
  maintenance: "Maintenance",
  offline: "Offline",
};

export const AMBULANCE_TYPE_LABELS = {
  basic: "Basic life support",
  advanced: "Advanced life support",
  icu: "Mobile ICU",
};

// The API sends UTC times without a "Z", so add it before converting to local time.
export function formatDateTime(value) {
  if (!value) return "-";
  const date = new Date(/[zZ]|[+-]\d\d:\d\d$/.test(value) ? value : value + "Z");
  return date.toLocaleString("en-IN", {
    day: "2-digit", month: "short", hour: "2-digit", minute: "2-digit", hour12: true,
  });
}

export const label = (map, key) => map[key] || key;
