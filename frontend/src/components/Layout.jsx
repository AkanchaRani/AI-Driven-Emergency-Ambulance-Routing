import { NavLink, Outlet } from "react-router-dom";
import { getHealth } from "../api/resources.js";
import useApi from "../hooks/useApi.js";

const NAV = [
  { to: "/", label: "Dashboard", end: true },
  { to: "/emergencies", label: "Emergency requests", end: true },
  { to: "/emergencies/new", label: "New request" },
  { to: "/ambulances", label: "Ambulances" },
  { to: "/hospitals", label: "Hospitals" },
];

export default function Layout() {
  const { data, error } = useApi(getHealth, []);
  const online = !!data && !error;

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">+</div>
          <div>
            <div className="brand-name">Ambulance Routing</div>
            <div className="brand-sub">Emergency control room</div>
          </div>
        </div>

        <nav className="nav">
          {NAV.map((item) => (
            <NavLink key={item.to} to={item.to} end={item.end}>
              {item.label}
            </NavLink>
          ))}
        </nav>

        <div className="sidebar-foot">
          <div className="conn">
            <span className={`dot ${online ? "dot-on" : "dot-off"}`} />
            {online ? "API and database connected" : "Backend not reachable"}
          </div>
          <div className="muted-light">MCA Final Year Project</div>
        </div>
      </aside>

      <main className="content">
        <Outlet />
      </main>
    </div>
  );
}
