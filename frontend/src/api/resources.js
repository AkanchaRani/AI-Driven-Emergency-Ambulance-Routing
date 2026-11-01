import { request } from "./client.js";

export const getDashboardSummary = () => request("/api/dashboard/summary");
export const listAmbulances = () => request("/api/ambulances");
export const listHospitals = () => request("/api/hospitals");
export const getHealth = () => request("/api/health");
