# SpecKit Constitution

## Project Identity

This repository contains the Jira/Confluence automation platform for ingesting, transforming, and publishing work-tracking data across Atlassian products. The system is built with a React 18 + Vite frontend, a Node.js + Express backend, and a PostgreSQL 15 database provisioned through Docker.

## Mission

The mission of this project is to deliver a reliable, maintainable, and auditable workflow that:

- Connects to Jira and Confluence data sources securely and predictably.
- Normalizes and validates incoming records before persistence or downstream processing.
- Provides a user-friendly web interface for report generation, workflow visibility, and operational control.
- Produces consistent, reviewable outputs for internal teams and external stakeholders.

## Core Principles

### 1. Human-readable, reviewable automation
All automation logic must be understandable by engineers who did not write it. Favor clear naming, small functions, descriptive comments where necessary, and intentional structure over clever one-liners.

### 2. Data integrity first
Every data flow must validate input, preserve provenance, and fail clearly when required fields or relationships are missing. Treat malformed Jira or Confluence payloads as normal integration risks.

### 3. Secure-by-default integration
Credentials, tokens, and sensitive configuration must never be hardcoded. Secrets must be supplied via environment variables or secure configuration stores. All integrations must support safe error handling and explicit audit logging.

### 4. Testable and observable behavior
Features must be implemented with verifiable outcomes. Prefer automated unit, integration, and API-level tests wherever practical. All substantial workflows must emit logs, metrics, or traces that enable debugging and operational review.

### 5. Consistent product delivery
The frontend, backend, and database layers must work together as a single system. Changes should be reviewed for API compatibility, schema impact, UI behavior, and deployment readiness before merge.

## Architecture Standards

### Frontend
- Use React 18 with Vite for the client application.
- Keep state management explicit and predictable; avoid excessive prop drilling and avoid hidden global side effects.
- Prefer reusable components, typed or well-documented data contracts, and clear separation between UI, services, and domain logic.
- Maintain a clean user experience for loading, error, and empty-state conditions.

### Backend
- Use Node.js with Express for application server responsibilities.
- Structure services around bounded responsibilities such as Jira integration, Confluence formatting, report generation, validation, and persistence.
- Route handlers should remain thin and delegate business logic to service modules.
- Handle failures consistently with meaningful HTTP responses, structured logging, and safe retries where appropriate.

### Data layer
- Use PostgreSQL 15 as the primary relational datastore.
- Manage schema changes deliberately, with versioned migrations and rollback awareness.
- Keep database access explicit, validated, and consistent with the application’s domain model.
- Avoid storing sensitive secrets in database tables unless that is an unavoidable requirement.

### Infrastructure and local development
- Use Docker for local PostgreSQL provisioning and any other local dependencies needed for reproducible environment setup.
- Keep environment configuration documented and aligned with the setup scripts used by the team.
- Ensure the project runs with a predictable local boot sequence and known dependency versions.

## Required Workflow

### 1. Define the change clearly
Before implementation, identify:
- the business outcome,
- affected systems,
- expected inputs and outputs,
- validation strategy,
- any data contract changes.

### 2. Build for compatibility
Every code change must consider:
- API contracts between frontend and backend,
- database schema and migration impact,
- configuration changes required by deployment,
- downstream consumers of generated reports or data.

### 3. Verify before completion
All non-trivial changes must be validated through relevant tests, linting, type checks, or manual verification steps as appropriate to the scope.

### 4. Document significant decisions
Any design choice that affects integration behavior, data shape, security posture, or operational reliability must be recorded in the repository in a way that is discoverable by future contributors.

## Quality Bar

### Code quality
- Favor small, focused modules over large monolithic files.
- Use consistent naming, formatting, and comment discipline.
- Remove dead code, stale configuration, and unused dependencies before merging.

### Testing expectations
- Add or update tests for new behaviors, especially for data validation, API contracts, and integration edge cases.
- Cover failure paths as well as success paths.
- Where possible, prefer real behavior tests over fragile mock-only assertions.

### Security and privacy
- Never expose secrets in logs, configuration snapshots, or repository artifacts.
- Validate user-controlled input before use.
- Restrict permissions, especially for operations that can create, modify, or delete records.

### Performance and reliability
- Design integrations and report generation to handle transient failures gracefully.
- Avoid unnecessary synchronous blocking in request handling.
- Use pagination, batching, or throttling when working with large Atlassian datasets.

## Change Control

### Scope discipline
Feature work should remain focused on the requested outcome. When additional scope emerges, it should be explicitly discussed and accepted before implementation expands.

### Risk awareness
Any change that affects schemas, authentication flows, external integrations, or report output must be reviewed with particular care. The expected behavior, failure modes, and rollback plan must be understood before deployment.

### Merge readiness
A change is ready to merge only when:
- implementation matches the intended design,
- tests or checks have been run,
- relevant documentation has been updated,
- no unresolved issues remain that would mislead users or operators.

## Operational Expectations

### Observability
The system should make it easy to answer:
- what request was processed,
- what data source it touched,
- what validation or transformation occurred,
- what result or error was returned.

### Maintainability
Contributors must be able to understand, extend, and safely modify the project without relying on undocumented tribal knowledge.

### Stability
The system should degrade predictably under invalid input, unavailable downstream services, or partial infrastructure failures, rather than crashing silently or producing inconsistent output.

## Final Rule

This project exists to make Jira and Confluence automation dependable, transparent, and maintainable. Every decision should be evaluated against that standard: clarity, correctness, security, and operational trustworthiness. 
