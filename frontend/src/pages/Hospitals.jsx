import { listHospitals } from "../api/resources.js";
import Notice from "../components/Notice.jsx";
import PageHeader from "../components/PageHeader.jsx";
import RefreshBar from "../components/RefreshBar.jsx";
import useApi from "../hooks/useApi.js";

export default function Hospitals() {
  const { data, error, loading, loadedAt, reload } = useApi(listHospitals, []);
  const yesNo = (v) => (v ? "Yes" : "No");

  return (
    <>
      <PageHeader title="Hospitals" subtitle="Hospital records stored in the database">
        <RefreshBar loadedAt={loadedAt} loading={loading} onRefresh={reload} />
      </PageHeader>
      {error && <Notice kind="error">{error}</Notice>}
      <Notice>Bed counts are entered manually. They are not checked against any real hospital system.</Notice>
      <section className="panel">
        {!data ? <div className="empty">Loading...</div> : (
          <div className="table-wrap">
            <table className="data-table">
              <thead>
                <tr><th>Hospital</th><th>Address</th><th>Beds available</th><th>ICU</th><th>Trauma centre</th></tr>
              </thead>
              <tbody>
                {data.map((h) => (
                  <tr key={h.id}>
                    <td>{h.name}</td>
                    <td>{h.address}</td>
                    <td>{h.available_beds} of {h.total_beds}</td>
                    <td>{yesNo(h.has_icu)}</td>
                    <td>{yesNo(h.has_trauma_centre)}</td>
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
