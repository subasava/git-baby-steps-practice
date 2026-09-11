const { loadReportData, validateReportData } = require('../services/reportService');
const { validateReportPayload } = require('../services/validationService');
const { renderHtmlReport } = require('../services/outputService');

async function getHealth(req, res) {
  res.json({ status: 'ok' });
}

async function getCurrentReport(req, res, next) {
  try {
    const report = loadReportData();
    const validation = validateReportPayload(report);

    if (!validation.valid) {
      return res.status(400).json({
        message: 'Report payload failed validation.',
        errors: validation.errors,
      });
    }

    res.json(report);
  } catch (error) {
    next(error);
  }
}

async function getSampleReport(req, res, next) {
  try {
    const report = loadReportData();
    res.json(report);
  } catch (error) {
    next(error);
  }
}

async function getHtmlReport(req, res, next) {
  try {
    const report = loadReportData();
    const validation = validateReportPayload(report);

    if (!validation.valid) {
      return res.status(400).json({
        message: 'Report payload failed validation.',
        errors: validation.errors,
      });
    }

    res.type('html').send(renderHtmlReport(report));
  } catch (error) {
    next(error);
  }
}

module.exports = {
  getHealth,
  getCurrentReport,
  getSampleReport,
  getHtmlReport,
};
