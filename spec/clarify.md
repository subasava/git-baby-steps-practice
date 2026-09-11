# Spec Review: Gaps, Contradictions, and Unclear Requirements

## 1. Review Summary

This review assesses the current constitution and specification for the Jira/Confluence automation project. The documents are strong on high-level principles and product intent, but several important implementation details are still ambiguous or inconsistent. These issues need to be resolved before engineering can proceed confidently.

## 2. Critical Gaps

### 2.1 Product scope is not fully defined

The repo currently mixes two different ideas:

- a status reporting solution for leadership and delivery management, and
- a broader Jira/Confluence automation platform.

The current documents do not clearly define whether the first release is:

1. a weekly reporting generator only,
2. a reusable data automation platform with reporting as one feature, or
3. a full operational workspace with shared data ingestion, storage, UI, and output generation.

This ambiguity affects architecture, roadmap, and acceptance criteria.

### 2.2 Source-of-truth model is unclear

The specification says the system should support:

- Jira issue data,
- Confluence page content,
- JSON fixtures for local dev,
- database-backed persisted status data.

However, it does not define the authoritative source model for production use.

Open questions:

- Is Jira/Confluence the primary source of truth, or is PostgreSQL the source of truth after ingestion?
- Is the system meant to read live Atlassian APIs continuously, or only on-demand?
- Is the database for normalized reporting data only, or does it also store raw source payloads?

### 2.3 Exact business workflow is not specified

The docs describe report generation, refresh data, and view current report state, but they do not define the exact workflow sequence end-to-end.

Missing details:

- when data sync happens,
- how reports are triggered,
- whether generation is manual, scheduled, or both,
- whether the UI is required for all actions or only for viewing,
- how users start a refresh and then generate a report.

### 2.4 Data mapping rules are underspecified

The specification says raw Jira and Confluence data should be normalized into a common schema, but it does not define how Jira issues, Confluence pages, statuses, comments, labels, milestones, and dependencies map into the internal data model.

Examples of missing rules:

- How does a Jira issue become a task, a dependency, or a milestone?
- How are Confluence pages used in the report—summary-only, extracted content, or linked metadata?
- How are custom Jira fields handled?
- What happens when a Jira issue is missing a required field like assignee or status?

### 2.5 Authentication and authorization model is incomplete

The constitution requires secure-by-default behavior, but the specification does not define:

- which authentication method is used for Jira and Confluence,
- whether the app uses user-scoped credentials or service-account credentials,
- how OAuth, API tokens, or personal access tokens are managed,
- whether multi-user role separation is part of v1.

This is a major missing requirement for a production-ready integration system.

### 2.6 Data retention and auditability requirements are missing

The constitution says the project should be auditable and observable, but the specification does not define:

- how long raw source payloads are retained,
- whether normalized data is immutable or overwritten,
- how validation failures are recorded,
- whether report generation history is stored,
- what audit metadata is required for each run.

### 2.7 Frontend behavior is not fully specified

The constitution says the frontend should be React 18 + Vite, but the specification does not define:

- page/component structure,
- dashboard screens,
- report editor or preview screens,
- user actions available in the interface,
- which workflows are required for the first release.

This means the UI architecture remains intentionally vague.

### 2.8 Backend API surface is not defined

The specification mentions API endpoints broadly, but it does not enumerate:

- endpoint names,
- request/response schemas,
- success/error payloads,
- status codes,
- pagination requirements,
- idempotency expectations.

Without this, backend and frontend integration cannot be implemented consistently.

### 2.9 Output artifact requirements are underspecified

The specification says HTML and PDF outputs are supported, but it does not define:

- required artifact filenames,
- file retention behavior,
- output destinations,
- preview behavior in the UI,
- what constitutes an acceptable PDF layout,
- whether HTML is generated at the same time as PDF or only on demand.

### 2.10 Deployment and environment expectations are incomplete

The docs state that PostgreSQL runs in Docker and environment variables are used, but they do not define:

- the exact local startup steps,
- required environment files,
- migration commands,
- how to run tests locally,
- how to handle Docker orchestration for the full stack.

### 2.11 Error handling policy is not sufficiently concrete

The specification says errors must be surfaced with enough context, but it does not define:

- retry policy,
- retry budget,
- backoff strategy,
- partial failure handling,
- whether failed report generation should still preserve partial results,
- whether invalid records are blocked entirely or stored for review.

### 2.12 Testing scope and evidence requirements are incomplete

The constitution requires testable and observable behavior, but the specification does not define:

- which test suites are mandatory,
- what level of coverage is expected,
- how integration tests are run against Dockerized PostgreSQL,
- what constitutes sufficient verification before merge.

## 3. Contradictions and Inconsistencies

### 3.1 Architecture mismatch with existing project artifacts

The constitution/specification describe a React 18 + Vite frontend, Node.js + Express backend, and PostgreSQL 15 via Docker.

But the earlier project specification file already describes a Python-based reporting solution with JSON input and HTML/PDF outputs.

That creates an inconsistency:

- Is the project being re-implemented in Node/React,
- or is the Python tool meant to continue as a component or legacy artifact?

This must be clarified before implementation begins.

### 3.2 Weekly report vs. general automation platform

The product summary frames the project as a Jira/Confluence automation platform, but much of the requirement language focuses on weekly status reporting only.

This creates a mismatch between:

- a broad automation platform scope, and
- a narrow reporting tool scope.

The system design should explicitly state whether the first release is user-facing reporting only or also includes general-purpose ingestion pipelines, transformations, and operational workflows.

### 3.3 Data refresh cadence is contradictory

The earlier project spec says the solution shall support a daily refresh cycle for underlying status data.

The current specification says the system will generate a weekly status report and includes refresh flows, but it does not clearly reconcile:

- daily refresh of source data,
- weekly report generation,
- on-demand generation,
- scheduled generation.

The relationship between refresh cadence and report cadence is not stated cleanly.

### 3.4 UI expectations are vague versus the stated product ambition

The specification says the frontend should provide a usable interface for report summaries, generated artifacts, data refresh, and error visibility.

Meanwhile, non-goals explicitly exclude real-time dashboards and multi-user collaboration.

This creates a tension:

- Is the front end a simple viewer/trigger application,
- or is it intended to support broader operational monitoring and collaboration features?

### 3.5 “Local JSON input” vs. “database-backed persisted status data”

The specification says the system should support JSON fixtures for local development and database-backed persisted status data, but it never clearly defines whether local JSON input is a temporary development path only or a production-supported path.

That leaves the production data flow unclear.

### 3.6 “JSON export or intermediate data artifacts” is optional but not well scoped

The specification says JSON export or intermediate data artifacts are supported where useful, but it does not define:

- when they should be produced,
- where they are stored,
- whether they are required for debugging only,
- whether they are part of the user-facing product.

### 3.7 Reporting output is described as both HTML and PDF, but PDF requirements are uncertain

The spec says PDF output is available when configured, but PDF details are not defined. This means the requirement is not yet concrete enough for implementation or acceptance.

### 3.8 “Data validation” versus “quarantine invalid data” is not fully specified

The spec says invalid or incomplete inputs should be rejected or quarantined for review, but the handling model is not defined.

Questions:

- Are invalid records rejected at the API layer or stored in a review queue?
- Can a report still be generated if only some records are invalid?
- Are partial failures allowed, or must the whole run fail?

## 4. Unclear Requirements

### 4.1 What exactly counts as a report?

The docs refer to a weekly status report, executive summary, and artifact outputs, but there is no formal definition of:

- required sections,
- mandatory fields,
- sorting rules,
- weighting of milestone risk,
- how dependencies are surfaced.

### 4.2 What is the canonical data schema?

The spec provides examples of report input JSON, but the full schema is not defined. It is unclear:

- which fields are required vs optional,
- field types,
- allowed enumerations for status values,
- validation logic for dates, owners, priorities, and severities.

### 4.3 What is the role of Confluence content?

The current docs mention Confluence page content, page metadata, and status notes, but they do not define:

- whether free-form Confluence content is parsed automatically,
- whether only summaries are extracted,
- whether content is stored raw or transformed,
- whether page structure matters.

### 4.4 What is the scope of Jira data integration?

The following are still unclear:

- whether only Jira Cloud is supported,
- whether Jira Server/Data Center is in scope,
- whether all issue types are included,
- whether subtasks, epics, and linked issues are treated the same,
- whether custom workflows and custom fields are supported in v1.

### 4.5 What does “current report state” mean?

The frontend is expected to show the current report state, but there is no definition of:

- what state is displayed,
- what fields are shown,
- whether the app shows the latest available source data, the last generated report, or both.

### 4.6 What is the definition of “validated data”?

The documents say validation must happen before persistence or report generation, but they do not define:

- severity levels for validation errors,
- which fields are mandatory,
- which validation failures are blocking vs non-blocking,
- how validation errors are represented to the user.

### 4.7 What is the expected user-facing workflow?

It is unclear whether the intended user flow is:

- UI-first,
- CLI-first,
- background job orchestration,
- or a hybrid.

This matters because the product design, API surface, and operations model all depend on it.

### 4.8 What is the expected role of PostgreSQL in production?

The documents say PostgreSQL is the primary datastore, but it is not clear:

- whether raw payloads are stored,
- whether all normalized records are persisted,
- whether there is a separate analytics/reporting schema,
- whether database writes are synchronous or asynchronous.

### 4.9 What does “safe retries” mean?

The constitution says safe retries where appropriate, but no retry policy is defined.

Open questions:

- How many retries are allowed?
- What is the timeout?
- Which endpoints are retried?
- Should the system skip retries for validation failures?

### 4.10 What is considered “production readiness” for v1?

The docs mention production readiness in the deployment section, but do not define release criteria for:

- environment separation,
- secrets handling,
- observability,
- logging retention,
- backup and recovery,
- rollback strategy.

## 5. Missing Decisions That Should Be Made Explicitly

Before implementation begins, the following decisions should be confirmed:

1. Is this a reporting application only, or a broader automation platform?
2. Is the first release UI-first, CLI-first, or hybrid?
3. Is PostgreSQL the system-of-record or only a reporting cache?
4. Are Jira and Confluence live integrations required for v1, or is local JSON input sufficient for the initial release?
5. What exact data is imported from Jira and Confluence?
6. What are the required fields, enums, and validation rules for the internal schema?
7. What is the exact report output contract for HTML and PDF?
8. What authentication and authorization model will be used for Atlassian integrations?
9. What operational policies apply for retries, failure handling, and audit retention?
10. What are the explicit acceptance criteria for UI, APIs, and generated reports?

## 6. Recommended Clarifying Questions for the Product Owner

1. Should the first release prioritize a weekly leadership reporting workflow, or a reusable cross-platform automation framework?
2. Do you want the system to support live Jira/Confluence pull on a schedule, or only manual refreshes for now?
3. Is PostgreSQL intended to store only normalized reporting data, or also raw ingested payloads?
4. Which Jira/Confluence fields are mandatory for version 1?
5. What is the exact minimum output for the report: HTML only, HTML + PDF, or other formats too?
6. Are there specific compliance, audit, or retention requirements for report history and source snapshots?
7. Do you want role-based access control in v1, or is the initial release single-user/single-tenant?
8. Should invalid records block whole report generation or allow partial report creation with warnings?
9. Is the existing Python solution being replaced, or should it remain as a legacy component alongside the new architecture?
10. Are there specific templates or branding requirements for executive-facing report output?

## 7. Suggested Resolution Order

The following items should be resolved first, in order:

1. scope definition,
2. source-of-truth and data lifecycle,
3. canonical schema and validation rules,
4. authentication and security model,
5. report generation contract,
6. API contract design,
7. UI workflow definition,
8. operational policies and testing expectations.

## 8. Bottom Line

The current constitution and specification have a strong foundation, but they are not yet implementation-ready. The biggest issues are scope ambiguity, missing canonical schema definitions, incomplete integration and security requirements, and unclear operational policies. These should be resolved before engineering begins in earnest.
