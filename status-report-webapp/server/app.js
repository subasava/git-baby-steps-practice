const express = require('express');
const cors = require('cors');
const reportsRoutes = require('./routes/reports');
const errorHandler = require('./middleware/errorHandler');

const app = express();

app.use(cors());
app.use(express.json());

app.get('/', (req, res) => {
  res.json({
    name: 'Status Report Web App API',
    status: 'running',
    endpoints: ['/api/health', '/api/reports/current', '/api/reports/html'],
  });
});

app.use('/api', reportsRoutes);
app.use(errorHandler);

module.exports = app;
