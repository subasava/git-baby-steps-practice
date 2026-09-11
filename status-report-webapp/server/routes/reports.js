const express = require('express');
const {
  getHealth,
  getCurrentReport,
  getSampleReport,
  getHtmlReport,
} = require('../controllers/reportController');

const router = express.Router();

router.get('/health', getHealth);
router.get('/reports/current', getCurrentReport);
router.get('/reports/sample', getSampleReport);
router.get('/reports/html', getHtmlReport);

module.exports = router;
