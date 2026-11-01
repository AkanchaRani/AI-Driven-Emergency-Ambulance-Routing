import { Navigate, Route, Routes } from "react-router-dom";
import Layout from "./components/Layout.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import NewEmergency from "./pages/NewEmergency.jsx";
import Emergencies from "./pages/Emergencies.jsx";
import EmergencyDetail from "./pages/EmergencyDetail.jsx";
import Ambulances from "./pages/Ambulances.jsx";
import Hospitals from "./pages/Hospitals.jsx";

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<Dashboard />} />
        <Route path="/emergencies" element={<Emergencies />} />
        <Route path="/emergencies/new" element={<NewEmergency />} />
        <Route path="/emergencies/:id" element={<EmergencyDetail />} />
        <Route path="/ambulances" element={<Ambulances />} />
        <Route path="/hospitals" element={<Hospitals />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  );
}
