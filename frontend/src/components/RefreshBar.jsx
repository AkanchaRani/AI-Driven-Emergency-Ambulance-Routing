// "Updated 3:42 pm" + Refresh button, used on pages that load data
export default function RefreshBar({ loadedAt, loading, onRefresh }) {
  return (
    <>
      {loadedAt && (
        <span className="muted small">
          Updated {loadedAt.toLocaleTimeString("en-IN", { hour: "2-digit", minute: "2-digit", second: "2-digit" })}
        </span>
      )}
      <button className="btn" onClick={onRefresh} disabled={loading}>
        {loading ? "Refreshing..." : "Refresh"}
      </button>
    </>
  );
}
