export default function ReportViewer({ report }) {
  if (!report) {
    return null;
  }

  const tasks = report.tasks || [];
  const risks = report.risks || [];
  const priorities = report.next_week_priorities || [];

  return (
    <div className="panel-grid">
      <div className="card panel">
        <h2>Current Work</h2>
        <table className="task-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Task</th>
              <th>Status</th>
              <th>Owner</th>
              <th>Priority</th>
              <th>Due</th>
              <th>Note</th>
            </tr>
          </thead>
          <tbody>
            {tasks.map((task) => (
              <tr key={task.id || task.title}>
                <td>{task.id}</td>
                <td>{task.title}</td>
                <td><span className="badge">{task.status}</span></td>
                <td>{task.owner}</td>
                <td>{task.priority}</td>
                <td>{task.due}</td>
                <td>{task.note}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="card panel">
        <h2>Risks & Dependencies</h2>
        <ul className="status-list">
          {risks.map((item, index) => <li key={`${item}-${index}`}>{item}</li>)}
        </ul>

        <h2 style={{ marginTop: '2rem' }}>Next Week's Priorities</h2>
        <ul className="status-list">
          {priorities.map((item, index) => <li key={`${item}-${index}`}>{item}</li>)}
        </ul>
      </div>
    </div>
  );
}
