# SpecKit Specification

## 1. Document Purpose

This specification defines the detailed requirements for the Jira/Confluence automation project described in the repository constitution. The system is intended to provide a repeatable, secure, and maintainable workflow for collecting data from Atlassian tools, validating and transforming it, storing it in PostgreSQL, and presenting it through a React 18 + Vite frontend with a Node.js + Express backend.

This document expands the project’s high-level goals into implementation-ready requirements, data contracts, integration expectations, quality gates, and acceptance criteria. 

## 2. Product Summary

The project will deliver a first release focused on a weekly status reporting workflow for Delivery Managers and leadership audiences, supported by Jira/Confluence automation. In v1, the system will:

- ingest data from Jira and Confluence sources,
- normalize and validate structure and content,
- persist approved data in PostgreSQL,
- expose a web-based interface for report workflows,
- generate readable executive outputs such as HTML reports and other publishable artifacts.

This is a scoped v1 implementation of a Jira/Confluence automation and reporting solution. It is intended to establish the core data pipeline, validation model, reporting engine, and review workflow. Broader platform features such as generic workflow automation, multi-user collaboration, advanced role management, and additional integrations are deferred to future phases.

## 3. Problem Statement

Teams managing delivery, migration, or cross-functional initiatives often struggle with fragmented status data spread across Jira issues, Confluence pages, and manually maintained reports. This causes:

- inconsistent weekly reporting,
- delayed visibility into blockers and risks,
- manual effort in recompiling updates for leadership,
- weak traceability between source data and published output.

The proposed system addresses these issues by establishing a structured workflow that turns Atlassian data into reliable, auditable reports.

## 4. Goals and Non-Goals

### 4.1 Goals

- Create a full-stack weekly reporting workflow for Jira and Confluence data ingestion.
- Provide a secure and observable backend service layer for data collection, validation, persistence, and report generation.
- Support PostgreSQL-backed persistence for reports, source snapshots, and normalized entities.
- Deliver a user-friendly React frontend for report review, output generation, and operational visibility.
- Generate executive-ready weekly reports from validated data.
- Design the solution so it can evolve from local JSON and manual inputs toward API/database-backed workflows.

### 4.2 Non-Goals

- A full-featured general-purpose automation platform in v1.
- Real-time dashboards in the initial release.
- Full multi-user collaboration and workflow approvals across all roles.
- Native support for every Atlassian product feature in v1.
- Automated email distribution in the initial release.
- Full enterprise SSO or advanced RBAC beyond basic project requirements unless explicitly added later.

## 5. Users and Personas

### 5.1 Delivery Manager

Represents the primary operational user, responsible for generating and reviewing weekly status reporting. Needs a dependable process to surface milestones, blockers, and dependencies clearly.

### 5.2 Leadership / Executives

Need concise and trustworthy summaries of delivery progress, risk posture, and priority items.

### 5.3 Team Leads / Functional Owners

Provide status data and help ensure ongoing accuracy of underlying Jira and Confluence content.

### 5.4 Technical Owner / Integrator

Owns configuration, data mappings, schema evolution, environment setup, and deployment reliability.

## 6. Core Use Cases

### 6.0 v1 Scope Decision

The first release will focus on a weekly reporting workflow. It includes the ability to pull Jira and Confluence data, normalize and validate it, store current state in PostgreSQL, generate a weekly report, and review or export the resulting artifact. The v1 scope does not include a general-purpose automation orchestration layer or broader multi-workflow platform capabilities.

### 6.1 Generate a Weekly Status Report

Actor: Delivery Manager

Flow:

1. The user opens the web app or runs the supported generation workflow.
2. The system loads status data from configured sources.
3. The backend validates and normalizes incoming data.
4. The system aggregates milestones, risks, dependencies, and progress indicators.
5. The frontend displays the report preview, and the system exports HTML or PDF output as configured.

### 6.2 Refresh Data from Jira and Confluence

Actor: Technical Owner

Flow:

1. The backend retrieves data from configured Jira and Confluence endpoints.
2. It stores a snapshot or normalized version in PostgreSQL.
3. Validation rules run before data is accepted for reporting.
4. Any errors or missing data are surfaced with actionable remediation details.

### 6.3 View Current Report State

Actor: Delivery Manager / Leadership

Flow:

1. The user opens the app dashboard.
2. The system loads the latest report metadata, summary, and status sections.
3. The user reviews progress, blockers, and upcoming priorities.

### 6.4 Handle Invalid or Incomplete Inputs

Actor: Technical Owner / System

Flow:

1. The system receives malformed, incomplete, or inconsistent data.
2. Input validation fails early with clear messages.
3. The data is rejected or quarantined for review.
4. The reporting process does not proceed with untrusted content.

## 7. Functional Requirements

### FR1. Input Sources

The system shall support structured data ingestion from:

- Jira issue data,
- Confluence page content,
- JSON-based fixture or sample input for local development,
- database-backed persisted status data.

### FR2. Data Normalization

The system shall normalize raw Jira and Confluence data into a common internal schema for:

- report metadata,
- workstream/task items,
- milestones,
- risks/issues,
- dependencies,
- next-week priorities.

### FR3. Validation

The system shall validate incoming entities before persistence or report generation. Validation must include required field checks, schema checks, and business-rule checks such as date consistency, ownership consistency, and status completeness.

### FR4. Persistence

The system shall persist normalized data in PostgreSQL 15 via Docker-managed infrastructure, including:

- report records,
- source snapshots,
- normalized entities,
- validation errors and audit metadata.

### FR5. Report Generation

The system shall generate a weekly status report containing:

- executive summary,
- completed vs. in-progress vs. blocked work,
- milestone progress,
- risks/issues/blockers,
- dependencies and handoffs,
- next-week priorities.

### FR6. Output Formats

The system shall support at least:

- HTML report output for review and sharing,
- PDF output when configured,
- JSON export or intermediate data artifacts where useful for debugging and automation.

### FR7. Web UI

The frontend shall provide a usable interface for:

- viewing report summaries,
- reviewing generated artifacts,
- updating or refreshing underlying source data,
- observing status and errors from the backend.

### FR8. Observability

The backend shall emit logs, errors, and metadata sufficient to trace:

- which source was processed,
- what was retrieved,
- what transformations were applied,
- what validation decisions were made,
- what output was produced.

### FR9. Configuration

The system shall support configuration through environment variables and configuration files, including:

- Jira connection details,
- Confluence access settings,
- PostgreSQL connection settings,
- output directories,
- feature flags for report generation and export.

### FR10. Error Handling

The system shall fail predictably and gracefully when integration endpoints are unavailable, credentials are invalid, or source data is incomplete. Errors must be surfaced with enough context for remediation.

## 8. Non-Functional Requirements

### NFR1. Usability

A non-technical user should be able to run routine report-generation workflows with minimal training. The UI and CLI should be understandable and self-explanatory.

### NFR2. Security

Secrets must be managed outside of source code. All external credentials must be loaded from environment variables or secure configuration stores. Sensitive data must not be exposed in logs or generated artifacts beyond what is strictly required.

### NFR3. Reliability

The system must validate input before generating output. Invalid inputs should stop the process cleanly rather than producing incomplete or misleading reports.

### NFR4. Extensibility

The project must be structured to allow additional connectors, transformation rules, and output formats without rewriting the core architecture.

### NFR5. Maintainability

Code must be organized into clear modules and layers. Business logic, integrations, validation, rendering, and persistence should remain separable.

### NFR6. Performance

The system should handle common report-generation workloads quickly and without unnecessary blocking. Large Jira/Confluence payloads should be processed with batching or pagination where practical.

### NFR7. Testability

Core workflows must be testable through unit, integration, and API-level tests. Tests should cover both success paths and failure paths.

## 9. System Architecture

### 9.1 Frontend

- React 18
- Vite-based development and build pipeline
- Componentized UI for report views and admin-related workflows
- Service layer for communicating with backend APIs

### 9.2 Backend

- Node.js + Express
- API endpoints for data retrieval, processing, validation, report generation, and output access
- Service-oriented modules for Jira integration, Confluence processing, validation, transformation, and persistence

### 9.3 Data Layer

- PostgreSQL 15
- Dockerized local environment for development
- Schema versioning via migrations
- Structured storage for normalized records and report metadata

### 9.4 Local Development Environment

- PostgreSQL running in Docker
- Local environment variables for secrets and configuration
- Reproducible boot sequence for developers

## 10. Data Model

### 10.1 Canonical Internal Schema

For v1, Jira and Confluence are the upstream data sources. PostgreSQL is the system of record for normalized, validated, report-ready data. The following canonical schema defines the internal representation used by the backend, frontend, and reporting engine.

#### Report

Represents a single generated weekly report instance.

Required fields:

- id: unique report identifier
- title: report title, typically "Weekly Status Report"
- report_date: ISO date for the reporting period
- summary: executive summary narrative
- status: enum such as draft, ready, generated, failed
- created_at: timestamp
- updated_at: timestamp
- source_metadata: JSON object containing source system metadata and run configuration

Optional fields:

- artifact_refs: references to generated HTML, PDF, or JSON outputs
- validation_summary: summary of validation warnings or blockers

#### Work Item / Task

Represents a tracked unit of work, typically sourced from Jira issues or normalized task records.

Required fields:

- id: unique task identifier
- external_id: original source identifier from Jira or another upstream source
- title: task title
- owner: accountable owner or assignee
- status: enum such as completed, in_progress, blocked, not_started
- priority: enum such as high, medium, low
- source_system: enum such as jira, confluence, json
- source_record: raw source payload or a reference to the normalized snapshot record

Optional fields:

- due_date: ISO date
- notes: free-form task notes
- labels: array of tags or labels
- related_issue_ids: array of linked Jira item identifiers

#### Milestone

Represents a major milestone or delivery checkpoint.

Required fields:

- id: unique milestone identifier
- name: milestone name
- target_date: ISO date
- status: enum such as on_track, at_risk, blocked, completed
- completion_percent: integer from 0 to 100
- source_system: enum such as jira, confluence, json

Optional fields:

- notes: milestone commentary
- external_id: original upstream identifier

#### Risk or Issue

Represents a risk, issue, or blocker surfaced in the weekly report.

Required fields:

- id: unique risk/issue identifier
- description: summary of the risk or issue
- owner: accountable owner
- severity: enum such as high, medium, low
- mitigation: mitigation plan or next action
- status: enum such as open, in_progress, mitigated, closed
- source_system: source of the record

Optional fields:

- external_id: original source identifier
- related_item_ids: related Jira or task references

#### Dependency

Represents a dependency or handoff requiring attention.

Required fields:

- id: unique dependency identifier
- description: dependency description
- owner: accountable owner
- status: enum such as blocked, at_risk, on_track, resolved
- action_required: clear next action or required support
- source_system: source system

Optional fields:

- external_id: original upstream identifier
- related_item_ids: related work references

#### Source Snapshot

Stores raw or near-raw upstream data to support observability and auditability.

Required fields:

- id: unique snapshot identifier
- source_system: jira or confluence
- source_type: issue, page, report, or other source category
- fetched_at: timestamp
- raw_payload: JSON object with the raw upstream record
- run_id: correlation identifier for the processing run

Optional fields:

- validation_status: pending, valid, invalid
- error_message: failure details if the fetch or parse failed

#### Validation Issue

Stores validation results for data that was rejected, corrected, or warned on.

Required fields:

- id: unique validation issue identifier
- entity_type: type of entity affected
- entity_id: affected internal identifier
- field: field that failed validation
- rule: validation rule name
- message: developer- and user-facing explanation
- severity: error or warning
- created_at: timestamp

Optional fields:

- suggested_fix: remediation guidance

### 10.2 Validation and Required-Field Rules

The following rules define the minimum validation contract for v1.

#### Required fields

- Every report must contain a title, report_date, summary, and status.
- Every task must contain a title, owner, status, priority, and source_system.
- Every milestone must contain a name, target_date, status, completion_percent, and source_system.
- Every risk/issue must contain a description, owner, severity, mitigation, status, and source_system.
- Every dependency must contain a description, owner, status, action_required, and source_system.

#### Data-type rules

- report_date, due_date, and target_date must be valid ISO dates.
- completion_percent must be an integer between 0 and 100.
- status and priority values must be restricted to documented enumerations.
- raw_payload and source_record must be JSON-compatible objects.

#### Business rules

- A report cannot be generated from invalid data if any required records fail validation.
- A task with status equal to blocked must include a clear note or dependency reference when available.
- A milestone with status at_risk or blocked must include a meaningful completion comment or supporting note.
- A dependency with status blocked must define action_required.
- Source snapshots must retain a run_id so each ingestion pass can be traced.

#### Validation behavior

- Validation shall run before persistence and before report generation.
- Validation errors shall be stored as Validation Issue records and surfaced through the API.
- Invalid records shall not silently overwrite previously accepted valid data.
- The system shall support warning-level validation for non-blocking data quality issues when appropriate.

### 10.3 Normalized Input Contract

The system should support a normalized JSON structure similar to the following:

```json
{
  "report": {
    "id": "report-2026-09-11",
    "title": "Weekly Status Report",
    "report_date": "2026-09-11",
    "summary": "Summary narrative",
    "status": "ready",
    "source_metadata": {
      "source_systems": ["jira", "confluence"],
      "run_id": "run-001"
    }
  },
  "tasks": [
    {
      "id": "task-001",
      "external_id": "JIRA-101",
      "title": "Finalize sprint planning",
      "owner": "Alex",
      "status": "completed",
      "priority": "high",
      "due_date": "2026-09-08",
      "notes": "Planning completed and approved by engineering leadership.",
      "source_system": "jira",
      "source_record": {
        "issueKey": "JIRA-101"
      }
    }
  ],
  "milestones": [
    {
      "id": "milestone-001",
      "name": "Migration phase 1",
      "target_date": "2026-09-30",
      "status": "on_track",
      "completion_percent": 65,
      "source_system": "jira"
    }
  ],
  "risks": [
    {
      "id": "risk-001",
      "description": "External API dependency is still pending",
      "owner": "Priya",
      "severity": "high",
      "mitigation": "Receive confirmation from the partner team.",
      "status": "open",
      "source_system": "confluence"
    }
  ],
  "dependencies": [
    {
      "id": "dependency-001",
      "description": "Partner team confirmation required",
      "owner": "Priya",
      "status": "blocked",
      "action_required": "Follow up with partner team and confirm timeline.",
      "source_system": "jira"
    }
  ],
  "next_week_priorities": [
    "Complete the stakeholder update workflow",
    "Resolve the external API dependency"
  ]
}
```

### 10.4 Output Contract

Generated reports should include:

- headline
- report date
- summary
- task status breakdown
- milestone overview
- risks/issues section
- dependencies and handoffs
- next-week priorities
- generated artifacts metadata
- validation summary, including any warnings or blockers encountered

### 10.5 Canonical Field Conventions

The following conventions apply across the canonical schema for v1:

- Use ISO 8601 date strings for dates and timestamps.
- Use lowercase enum values for status and source identifiers where practical.
- Keep source identifiers separate from internal identifiers.
- Preserve provenance with source_system, external_id, and source_record metadata.
- Keep validation errors distinct from generated report content.

## 11. Integration Requirements

### 11.1 Jira Integration

For v1, the system shall support authenticated read access to Jira data using configured credentials stored outside of source control. The system will consume Jira issue metadata needed for weekly reporting, including:

- issue summaries,
- status fields,
- assignees,
- due dates,
- labels/tags,
- links to related work,
- issue hierarchy or related issue references where available.

The minimum fields required for a Jira issue to be usable in v1 are:

- issue key or equivalent unique identifier,
- summary/title,
- status,
- assignee or owner,
- updated timestamp,
- project context where needed for reporting.

The system shall treat unsupported or unavailable Jira fields as optional unless they are explicitly required for a report section.

### 11.2 Confluence Integration

For v1, the system shall support authenticated read access to Confluence content using configured credentials stored outside of source control. The system shall consume Confluence page metadata and summaries needed for weekly reporting, including:

- page titles,
- page metadata,
- page content summaries,
- status notes and updates,
- references to related Jira items.

The minimum fields required for a Confluence page to be usable in v1 are:

- page identifier,
- page title,
- updated timestamp,
- content summary or structured content excerpt,
- related Jira references where available.

The system shall support Confluence content ingestion in a structured manner, but it does not need to process every possible Confluence document format in v1. Advanced page transformation, rich content parsing, or deep document analytics are considered out of scope unless explicitly added later.

### 11.3 Atlassian Authentication and Secret Handling

v1 shall use environment-variable-based configuration for Jira and Confluence authentication. Secrets must never be stored in source code, committed configuration files, or generated artifacts.

Accepted v1 authentication assumptions:

- Jira and Confluence access shall use configured API credentials or tokens provided through secure environment configuration.
- The application shall fail clearly when required credentials are missing, expired, or invalid.
- The system shall support separate configuration for development, testing, and production environments.

The system shall not assume user-interactive login flows in v1. For this release, the project is scoped to service-backed, automated integrations rather than interactive end-user Atlassian authentication.

### 11.4 Out-of-Scope Atlassian Features for v1

The following Atlassian capabilities are explicitly out of scope for v1 unless separately approved:

- full custom-field mapping for every Jira field type,
- advanced Confluence page transformation beyond content summaries and metadata extraction,
- general workflow orchestration across Atlassian products,
- enterprise-level access-control or SSO integration beyond basic configuration management,
- multi-user collaboration or approval workflows in the Atlassian integration layer.

### 11.5 Integration Failure Handling

The system shall handle Atlassian integration failures predictably and with enough context for remediation. The following failure modes are in scope for v1:

- invalid or expired credentials,
- missing required fields in an API response,
- partial data payloads,
- unavailable Atlassian services,
- rate-limit or quota-related errors.

For each failure mode, the system shall:

- return a clear, actionable error message,
- persist the failure metadata and run context,
- avoid silently corrupting previously accepted valid records,
- preserve enough information for a technical owner to investigate and correct the issue.

### 11.6 API Contract Expectations

The backend should expose stable endpoints for:

- fetching source data,
- triggering report generation,
- retrieving report results,
- querying validation errors,
- retrieving persisted report metadata.

## 12. User Stories

### US1
As a Delivery Manager, I want to generate weekly reports from current source data so that leadership sees consistent updates.

### US2
As a Technical Owner, I want validation to run before report creation so that bad data does not produce misleading artifacts.

### US3
As a Leadership User, I want a concise report with risks and dependencies so that I can make timely decisions.

### US4
As a Team Lead, I want source data refreshed from Jira and Confluence so that team information remains current.

### US5
As a Developer, I want modular architecture so that new integrations and output formats can be added without rewriting the system.

## 13. Failure Modes and Edge Cases

- Jira or Confluence API returns incomplete content.
- Credentials are missing or expired.
- A required field is absent from source data.
- Dates are malformed or inconsistent.
- Report generation is requested for a date range with no data.
- PostgreSQL is unavailable.
- PDF export is requested but rendering dependency is missing.

For each failure mode, the system should produce a clear error message, store relevant metadata, and avoid partial or misleading output.

## 14. Quality Gates

The following checks should be satisfied before a change is considered complete:

- automated tests for relevant logic pass,
- backend API behavior has been validated,
- data validation rules have been exercised,
- output artifacts are reviewed for readability,
- configuration changes are documented,
- no secrets are committed to source control.

## 15. Testing Strategy

### 15.1 Unit Tests

Cover:

- data normalization,
- validation rules,
- transformation logic,
- output rendering helpers.

### 15.2 Integration Tests

Cover:

- API endpoints,
- PostgreSQL persistence,
- fetch and normalize flows from sample Jira/Confluence payloads,
- report generation end-to-end.

### 15.3 Manual Verification

Verify:

- the UI loads correctly,
- reports render properly,
- Docker-based PostgreSQL setup works,
- generated artifacts are present and readable.

## 16. Deployment and Environment Expectations

### 16.1 Development

- PostgreSQL runs in Docker.
- Frontend runs through Vite.
- Backend runs through Node.js + Express.
- Local environment variables configure integrations and database access.

### 16.2 Production Readiness

The initial design should support:

- secure configuration management,
- deployment-friendly environment separation,
- migration-based schema evolution,
- log retention and basic observability,
- restart-safe service behavior.

## 17. Acceptance Criteria

The project is considered complete when all of the following are true:

1. A user can load source data from Jira and/or Confluence into the system.
2. The system normalizes and validates incoming data before persistence.
3. Data is stored in PostgreSQL and is retrievable through the backend.
4. A weekly status report can be generated from stored or fresh source data.
5. The report contains milestone, risk, dependency, and next-priority sections.
6. HTML and PDF outputs are available as configured.
7. The frontend demonstrates the current report state and report generation workflow.
8. Invalid input produces clear, actionable errors.
9. Secrets are not stored in source control.
10. The local development environment works reliably with Dockerized PostgreSQL.

## 18. Risks and Mitigations

### Risk: Inconsistent Source Quality
Mitigation: schema validation, required-field enforcement, and staging of invalid records.

### Risk: Unavailable External Services
Mitigation: explicit error handling, retries where appropriate, and clear operator-facing messaging.

### Risk: Reporting Becomes Manual Again
Mitigation: simple workflows, clear UI, and automation hooks for recurring tasks.

### Risk: Data Model Drift
Mitigation: versioned schema changes, migration discipline, and backward-compatible transformations.

## 19. Open Questions

- Should the first version support only weekly generation, or also on-demand generation?
- Is the initial source of truth a local JSON file, an API, or a database-backed sync process?
- Are there required Atlassian fields beyond the basic task, milestone, risk, and dependency model?
- Should the system support direct export to shared leadership channels in the first release?

## 20. Recommended Next Steps

1. Finalize the normalized report schema.
2. Define the PostgreSQL schema and migration plan.
3. Implement the backend API surface.
4. Build the React frontend around the report lifecycle.
5. Add validation, error handling, and output generation.
6. Verify end-to-end with sample Jira/Confluence inputs and Dockerized PostgreSQL.

## 21. Final Requirement Statement

The Jira/Confluence automation project must deliver a secure, maintainable, and testable full-stack solution that collects Atlassian data, validates and stores it in PostgreSQL, and provides a consistent reporting workflow through a React frontend and Express backend.
