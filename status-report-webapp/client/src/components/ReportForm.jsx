export default function ReportForm({ onRefresh }) {
  return (
    <div className="card summary-box">
      <h2>Report Controls</h2>
      <p style={{ marginTop: 0, color: '#475569' }}>
        Refresh the latest sample report payload from the backend and review the generated summary.
      </p>
      <button className="button" onClick={onRefresh}>Refresh report data</button>
    </div>
  );
}
