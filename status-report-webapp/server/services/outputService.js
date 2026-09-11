function renderHtmlReport(report) {
  const taskRows = (report.tasks || [])
    .map((task) => `
      <tr>
        <td>${task.id || ''}</td>
        <td>${task.title || ''}</td>
        <td>${task.status || ''}</td>
        <td>${task.owner || ''}</td>
        <td>${task.priority || ''}</td>
        <td>${task.due || ''}</td>
        <td>${task.note || ''}</td>
      </tr>
    `)
    .join('');

  return `<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>${report.headline || 'Weekly Status Report'}</title>
    <style>
      body { font-family: Arial, sans-serif; margin: 2rem; color: #111827; }
      h1 { margin-bottom: 0.5rem; }
      .summary { background: #f3f4f6; border-left: 4px solid #2563eb; padding: 1rem; margin-bottom: 1.5rem; }
      table { width: 100%; border-collapse: collapse; margin-top: 1rem; }
      th, td { border-bottom: 1px solid #d1d5db; padding: 0.75rem; text-align: left; }
      th { background: #f8fafc; }
      ul { padding-left: 1.25rem; }
    </style>
  </head>
  <body>
    <h1>${report.headline || 'Weekly Status Report'}</h1>
    <p><strong>Report Date:</strong> ${report.report_date || ''}</p>

    <div class="summary">
      ${report.summary || 'No summary provided.'}
    </div>

    <h2>Current Work</h2>
    <table>
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
        ${taskRows}
      </tbody>
    </table>

    <h2>Risks</h2>
    <ul>
      ${(report.risks || []).map((item) => `<li>${item}</li>`).join('')}
    </ul>

    <h2>Next Week's Priorities</h2>
    <ul>
      ${(report.next_week_priorities || []).map((item) => `<li>${item}</li>`).join('')}
    </ul>
  </body>
</html>`;
}

module.exports = {
  renderHtmlReport,
};
