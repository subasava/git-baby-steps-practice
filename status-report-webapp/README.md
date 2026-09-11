# Status Report Web App

This project now includes a runnable full-stack setup for the weekly status reporting workflow.

## Run locally

1. Start PostgreSQL via Docker:
   `docker compose up db`
2. Start the backend:
   `cd status-report-webapp/server && npm install && npm run dev`
3. Start the frontend:
   `cd status-report-webapp/client && npm install && npm run dev`
4. Open http://localhost:5173

## Run everything with Docker Compose from the workspace root

```bash
docker compose up --build
```

The frontend will proxy `/api` requests to the backend service, and the backend will read the bundled sample report payload from `status-report-webapp/server/data/sampleReport.json`.
