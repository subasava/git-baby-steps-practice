import { useMemo } from 'react';
import ReportForm from '../components/ReportForm';
import ReportViewer from '../components/ReportViewer';
import SummaryCard from '../components/SummaryCard';
import useReportData from '../hooks/useReportData';

export default function DashboardPage() {
  const { report, loading, error, reload } = useReportData();

  const metrics = useMemo(() => {
    if (!report || !Array.isArray(report.tasks)) {
      return {
        completed: 0,
        inProgress: 0,
        blocked: 0,
        notStarted: 0,
      };
    }

    return report.tasks.reduce(
      (acc, task) => {
        if (task.status === 'Completed') acc.completed += 1;
        if (task.status === 'In Progress') acc.inProgress += 1;
        if (task.status === 'Blocked') acc.blocked += 1;
        if (task.status === 'Not Started') acc.notStarted += 1;
        return acc;
      },
      { completed: 0, inProgress: 0, blocked: 0, notStarted: 0 },
    );
  }, [report]);

  return (
    <div className="dashboard">
      <div className="topbar">
        <h1>Weekly Status Report</h1>
        <button className="button secondary" onClick={reload}>
          Reload
        </button>
      </div>

      {loading && <div className="loading">Loading report data...</div>}
      {error && <div className="error">Error: {error}</div>}

      {report && (
        <>
          <ReportForm onRefresh={reload} />

          <div className="metrics">
            <SummaryCard title="Completed" value={metrics.completed} />
            <SummaryCard title="In Progress" value={metrics.inProgress} />
            <SummaryCard title="Blocked" value={metrics.blocked} />
            <SummaryCard title="Not Started" value={metrics.notStarted} />
          </div>

          <div className="card summary-box">
            <h2>{report.headline}</h2>
            <p style={{ margin: '0.5rem 0', color: '#475569' }}><strong>Reporting date:</strong> {report.report_date}</p>
            <p style={{ marginBottom: 0 }}>{report.summary}</p>
          </div>

          <ReportViewer report={report} />
        </>
      )}
    </div>
  );
}
