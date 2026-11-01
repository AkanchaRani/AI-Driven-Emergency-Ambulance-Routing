import { useState } from "react";
import { Link } from "react-router-dom";
import { listEmergencies } from "../api/emergencies.js";
import EmergencyTable from "../components/EmergencyTable.jsx";
import Notice from "../components/Notice.jsx";
import PageHeader from "../components/PageHeader.jsx";
import RefreshBar from "../components/RefreshBar.jsx";
import useApi from "../hooks/useApi.js";
import { SEVERITY_LABELS, STATUS_LABELS } from "../utils/format.js";

export default function Emergencies() {
  const [status, setStatus] = useState("");
  const [severity, setSeverity] = useState("");
  const { data, error, loading, loadedAt, reload } = useApi(
    () => listEmergencies({ status, severity }),
    [status, severity]
  );

  return (
    <>
      <PageHeader title="Emergency requests" subtitle="Newest requests first">
        <RefreshBar loadedAt={loadedAt} loading={loading} onRefresh={reload} />
        <Link to="/emergencies/new" className="btn btn-primary">New request</Link>
      </PageHeader>

      <div className="filters">
        <label>
          Status
          <select value={status} onChange={(e) => setStatus(e.target.value)}>
            <option value="">All</option>
            {Object.entries(STATUS_LABELS).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
          </select>
        </label>
        <label>
          Severity
          <select value={severity} onChange={(e) => setSeverity(e.target.value)}>
            <option value="">All</option>
            {Object.entries(SEVERITY_LABELS).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
          </select>
        </label>
        {data && <span className="muted small">{data.total} request(s)</span>}
      </div>

      {error && <Notice kind="error">{error}</Notice>}
      <section className="panel">
        {data ? <EmergencyTable items={data.items} /> : !error && <div className="empty">Loading...</div>}
      </section>
    </>
  );
}
