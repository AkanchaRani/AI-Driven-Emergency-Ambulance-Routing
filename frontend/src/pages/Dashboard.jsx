import { Link } from "react-router-dom";
import { listEmergencies } from "../api/emergencies.js";
import { getDashboardSummary, listAmbulances } from "../api/resources.js";
import { AmbulanceStatusBadge } from "../components/Badges.jsx";
import EmergencyTable from "../components/EmergencyTable.jsx";
import Notice from "../components/Notice.jsx";
import PageHeader from "../components/PageHeader.jsx";
import RefreshBar from "../components/RefreshBar.jsx";
import useApi from "../hooks/useApi.js";
import { STATUS_LABELS, label } from "../utils/format.js";

async function loadDashboard() {
  const [summary, emergencies, ambulances] = await Promise.all([
    getDashboardSummary(),
    listEmergencies({ limit: 100 }),
    listAmbulances(),
  ]);
  return { summary, emergencies: emergencies.items, ambulances };
}

export default function Dashboard() {
  const { data, error, loading, loadedAt, reload } = useApi(loadDashboard, []);

  const header = (
    <PageHeader title="Dashboard" subtitle="Live figures from the MySQL database">
      <RefreshBar loadedAt={loadedAt} loading={loading} onRefresh={reload} />
    </PageHeader>
  );

  if (error) return <>{header}<Notice kind="error">{error}</Notice></>;
  if (!data) return <>{header}<div className="empty">Loading...</div></>;

  const { summary, emergencies, ambulances } = data;
  const active = emergencies.filter((e) => !["completed", "cancelled"].includes(e.status));

  return (
    <>
      {header}

      <div className="stat-strip">
        <div className="stat">
          <div className="stat-value">{summary.total_emergencies}</div>
          <div className="stat-label">Total requests</div>
        </div>
        <div className="stat">
          <div className="stat-value">{summary.active_emergencies}</div>
          <div className="stat-label">Active requests</div>
        </div>
        <div className="stat">
          <div className="stat-value text-critical">{summary.by_status.pending || 0}</div>
          <div className="stat-label">Waiting for assignment</div>
        </div>
        <div className="stat">
          <div className="stat-value text-ok">{summary.ambulances_available}</div>
          <div className="stat-label">Ambulances available (of {summary.ambulances_total})</div>
        </div>
        <div className="stat">
          <div className="stat-value">{summary.hospitals_total}</div>
          <div className="stat-label">Hospitals registered</div>
        </div>
      </div>

      <div className="two-col">
        <section className="panel">
          <div className="panel-head">
            <h2>Active emergency requests</h2>
            <Link to="/emergencies">View all requests</Link>
          </div>
          <EmergencyTable
            items={active.slice(0, 8)}
            emptyText="No active requests right now."
          />
        </section>

        <div className="stack">
          <section className="panel">
            <div className="panel-head"><h2>Requests by status</h2></div>
            <table className="data-table compact">
              <tbody>
                {Object.keys(STATUS_LABELS).map((key) => (
                  <tr key={key}>
                    <td>{label(STATUS_LABELS, key)}</td>
                    <td className="num">{summary.by_status[key] || 0}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </section>

          <section className="panel">
            <div className="panel-head">
              <h2>Ambulances</h2>
              <Link to="/ambulances">Details</Link>
            </div>
            <table className="data-table compact">
              <tbody>
                {ambulances.map((a) => (
                  <tr key={a.id}>
                    <td>{a.registration_number}</td>
                    <td className="num"><AmbulanceStatusBadge value={a.status} /></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </section>
        </div>
      </div>
    </>
  );
}
