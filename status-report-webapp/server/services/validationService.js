function validateReportPayload(report) {
  const errors = [];

  if (!report || typeof report !== 'object' || Array.isArray(report)) {
    return { valid: false, errors: ['Report payload must be an object.'] };
  }

  const requiredTopLevelFields = ['headline', 'report_date', 'summary', 'tasks'];

  for (const field of requiredTopLevelFields) {
    if (!(field in report)) {
      errors.push(`Missing required field: ${field}`);
    }
  }

  if (!Array.isArray(report.tasks)) {
    errors.push('Field "tasks" must be an array.');
  }

  if (Array.isArray(report.tasks)) {
    for (let index = 0; index < report.tasks.length; index += 1) {
      const task = report.tasks[index];
      if (!task || typeof task !== 'object') {
        errors.push(`Task at index ${index} must be an object.`);
        continue;
      }

      ['id', 'title', 'status', 'owner', 'priority', 'due', 'note'].forEach((field) => {
        if (!(field in task)) {
          errors.push(`Task at index ${index} is missing required field: ${field}`);
        }
      });
    }
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}

module.exports = {
  validateReportPayload,
};
