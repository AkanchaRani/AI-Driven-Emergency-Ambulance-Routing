import { useState } from "react";
import { Link, useParams } from "react-router-dom";
import { getEmergency, updateEmergencyStatus } from "../api/emergencies.js";
import { SeverityBadge, StatusBadge } from "../components/Badges.jsx";
import Notice from "../components/Notice.jsx";
import PageHeader from "../components/PageHeader.jsx";
import RefreshBar from "../components/RefreshBar.jsx";
import useApi from "../hooks/useApi.js";
import { STATUS_LABELS, TYPE_LABELS, formatDateTime, label } from "../utils/format.js";

function Row({ term, children }) {
  return (
    <>
      <dt>{term}</dt>
      <dd>{children || "-"}</dd>
    </>
  );
}

export default function EmergencyDetail() {
  const { id } = useParams();
  const { data: e, error, loading, loadedAt, reload } = useApi(() => getEmergency(id), [id]);
  const [nextStatus, setNextStatus] = useState("");
  const [remarks, setRemarks] = useState("");
  const [updating, setUpdating] = useState(false);
  const [updateError, setUpdateError] = useState("");
  const [message, setMessage] = useState("");

  async function handleUpdate(ev) {
    ev.preventDefault();
    if (!nextStatus) return;
    setUpdating(true);
    setUpdateError("");
    setMessage("");
    try {
      await updateEmergencyStatus(id, nextStatus, remarks);
      setMessage(`Status changed to ${label(STATUS_LABELS, nextStatus)}.`);
      setNextStatus("");
      setRemarks("");
      await reload();
    } catch (err) {
      setUpdateError(err.message);
    } finally {
      setUpdating(false);
    }
  }

  const header = (
    <PageHeader title={`Emergency request #${id}`}>
      <RefreshBar loadedAt={loadedAt} loading={loading} onRefresh={reload} />
      <Link to="/emergencies" className="btn">Back to list</Link>
    </PageHeader>
  );

  if (error) return <>{header}<Notice kind="error">{error}</Notice></>;
  if (!e) return <>{header}<div className="empty">Loading...</div></>;

  return (
    <>
      {header}
      <div className="two-col detail">
        <section className="panel">
          <div className="panel-head">
            <h2>Request details</h2>
            <span><SeverityBadge value={e.severity} /> <StatusBadge value={e.status} /></span>
          </div>
          <dl className="details">
            <Row term="Emergency type">{label(TYPE_LABELS, e.emergency_type)}</Row>
            <Row term="Pickup location">{e.location_address}</Row>
            <Row term="Coordinates">
              {e.latitude != null ? `${e.latitude}, ${e.longitude}` : null}
            </Row>
            <Row term="Caller">{e.caller_name} ({e.caller_phone})</Row>
            <Row term="Patient">
              {[e.patient_name, e.patient_age != null ? `${e.patient_age} yrs` : null, e.patient_gender]
                .filter(Boolean).join(", ")}
            </Row>
            <Row term="Notes">{e.description}</Row>
            <Row term="Registered">{formatDateTime(e.created_at)}</Row>
            <Row term="Last updated">{formatDateTime(e.updated_at)}</Row>
          </dl>
        </section>

        <div className="stack">
          <section className="panel">
            <div className="panel-head"><h2>Update status</h2></div>
            {message && <Notice kind="success">{message}</Notice>}
            {updateError && <Notice kind="error">{updateError}</Notice>}
            {e.allowed_next_statuses.length === 0 ? (
              <p className="muted pad">This request is closed. Its status cannot be changed.</p>
            ) : (
              <form className="form pad" onSubmit={handleUpdate}>
                <div className="field">
                  <label htmlFor="next_status">New status</label>
                  <select id="next_status" value={nextStatus} onChange={(ev) => setNextStatus(ev.target.value)}>
                    <option value="">Select status</option>
                    {e.allowed_next_statuses.map((s) => (
                      <option key={s} value={s}>{label(STATUS_LABELS, s)}</option>
                    ))}
                  </select>
                </div>
                <div className="field">
                  <label htmlFor="remarks">Remarks (optional)</label>
                  <input id="remarks" value={remarks} maxLength={255} onChange={(ev) => setRemarks(ev.target.value)} />
                </div>
                <button className="btn btn-primary" disabled={!nextStatus || updating}>
                  {updating ? "Updating..." : "Update status"}
                </button>
                <p className="hint">Ambulance assignment is not automated yet, so the status is changed by hand.</p>
              </form>
            )}
          </section>

          <section className="panel">
            <div className="panel-head"><h2>Status history</h2></div>
            <table className="data-table compact">
              <thead>
                <tr><th>Time</th><th>Change</th><th>Remarks</th></tr>
              </thead>
              <tbody>
                {[...e.status_history].reverse().map((h) => (
                  <tr key={h.id}>
                    <td className="nowrap">{formatDateTime(h.changed_at)}</td>
                    <td>
                      {h.old_status ? `${label(STATUS_LABELS, h.old_status)} to ` : ""}
                      {label(STATUS_LABELS, h.new_status)}
                    </td>
                    <td>{h.remarks || "-"}</td>
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
