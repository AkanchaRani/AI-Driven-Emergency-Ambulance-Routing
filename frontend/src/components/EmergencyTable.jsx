import { Link } from "react-router-dom";
import { SeverityBadge, StatusBadge } from "./Badges.jsx";
import { TYPE_LABELS, formatDateTime, label } from "../utils/format.js";

export default function EmergencyTable({ items, emptyText }) {
  if (!items.length) {
    return <div className="empty">{emptyText || "No emergency requests found."}</div>;
  }
  return (
    <div className="table-wrap">
      <table className="data-table emergencies">
        <thead>
          <tr>
            <th>ID</th>
            <th>Severity</th>
            <th>Type</th>
            <th>Location</th>
            <th>Caller</th>
            <th>Status</th>
            <th>Registered</th>
          </tr>
        </thead>
        <tbody>
          {items.map((e) => (
            <tr key={e.id}>
              <td><Link to={`/emergencies/${e.id}`}>#{e.id}</Link></td>
              <td><SeverityBadge value={e.severity} /></td>
              <td>{label(TYPE_LABELS, e.emergency_type)}</td>
              <td>{e.location_address}</td>
              <td>{e.caller_name}<div className="muted small">{e.caller_phone}</div></td>
              <td><StatusBadge value={e.status} /></td>
              <td className="nowrap">{formatDateTime(e.created_at)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
