import { listAmbulances } from "../api/resources.js";
import { AmbulanceStatusBadge } from "../components/Badges.jsx";
import Notice from "../components/Notice.jsx";
import PageHeader from "../components/PageHeader.jsx";
import RefreshBar from "../components/RefreshBar.jsx";
import useApi from "../hooks/useApi.js";
import { AMBULANCE_TYPE_LABELS, formatDateTime, label } from "../utils/format.js";

export default function Ambulances() {
  const { data, error, loading, loadedAt, reload } = useApi(listAmbulances, []);

  return (
    <>
      <PageHeader title="Ambulances" subtitle="Fleet records stored in the database">
        <RefreshBar loadedAt={loadedAt} loading={loading} onRefresh={reload} />
      </PageHeader>
      {error && <Notice kind="error">{error}</Notice>}
      <Notice>Positions are the last values entered in the database. Live GPS tracking is not integrated yet.</Notice>
      <section className="panel">
        {!data ? <div className="empty">Loading...</div> : (
          <div className="table-wrap">
            <table className="data-table">
              <thead>
                <tr><th>Registration</th><th>Type</th><th>Status</th><th>Base hospital</th><th>Last known position</th><th>Updated</th></tr>
              </thead>
              <tbody>
                {data.map((a) => (
                  <tr key={a.id}>
                    <td>{a.registration_number}</td>
                    <td>{label(AMBULANCE_TYPE_LABELS, a.ambulance_type)}</td>
                    <td><AmbulanceStatusBadge value={a.status} /></td>
                    <td>{a.base_hospital_name || "-"}</td>
                    <td>{a.current_latitude != null ? `${a.current_latitude}, ${a.current_longitude}` : "-"}</td>
                    <td className="nowrap">{formatDateTime(a.updated_at)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </>
  );
}
