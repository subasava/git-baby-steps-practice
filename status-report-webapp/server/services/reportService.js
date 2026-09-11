const fs = require('fs');
const path = require('path');
const { reportDataFile } = require('../config/env');

function loadReportData(filePath = reportDataFile) {
  const resolvedPath = path.resolve(filePath);

  if (!fs.existsSync(resolvedPath)) {
    throw new Error(`Report data file not found: ${resolvedPath}`);
  }

  const raw = fs.readFileSync(resolvedPath, 'utf-8');
  const parsed = JSON.parse(raw);

  return parsed;
}

module.exports = {
  loadReportData,
};
