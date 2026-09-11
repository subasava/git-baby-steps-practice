const path = require('path');
const dotenv = require('dotenv');

dotenv.config({ path: path.resolve(__dirname, '..', '.env') });

module.exports = {
  port: Number(process.env.PORT || 3001),
  reportDataFile: process.env.REPORT_DATA_FILE || path.resolve(__dirname, '..', 'data', 'sampleReport.json'),
};
