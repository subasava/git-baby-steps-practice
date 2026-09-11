const app = require('./app');
const { port } = require('./config/env');

app.listen(port, () => {
  console.log(`Status Report API listening on http://localhost:${port}`);
});
