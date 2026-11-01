import { request } from "./client.js";

export const createEmergency = (data) =>
  request("/api/emergencies", { method: "POST", body: JSON.stringify(data) });

export const listEmergencies = ({ status, severity, limit = 100 } = {}) => {
  const params = new URLSearchParams({ limit });
  if (status) params.set("status", status);
  if (severity) params.set("severity", severity);
  return request(`/api/emergencies?${params}`);
};

export const getEmergency = (id) => request(`/api/emergencies/${id}`);

export const updateEmergencyStatus = (id, status, remarks) =>
  request(`/api/emergencies/${id}/status`, {
    method: "PATCH",
    body: JSON.stringify({ status, remarks: remarks || null }),
  });
