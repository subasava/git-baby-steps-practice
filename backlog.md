# Status Reporting Solution Implementation Backlog

This backlog is derived from [project_spec.md](project_spec.md) and reflects the choices made during planning:

- Prioritize a complete MVP first
- Keep the first release focused on JSON input with a basic CLI
- Include PDF generation in the first release
- Use the spec’s phased structure: Setup, Core Features, Integration, Testing, Documentation

## Phase 1: Setup


Note: Jira MCP can assist with Jira issue tracking and project metadata workflows, but it cannot perform the implementation tasks in this backlog directly. All items below are therefore marked as Custom Skill.

- [ ] Confirm the current baseline implementation and identify what should be preserved from the existing Python CLI and sample JSON workflow (Custom Skill) — Approach 1
- [ ] Define the target project structure for the MVP, including modules for input loading, validation, transformation, rendering, output generation, and CLI entry points (Custom Skill) — Approach 1
- [ ] Create a clear, machine-readable input schema contract for the weekly status report JSON payload so it can be implemented and validated by a coding agent without ambiguity. Define the authoritative schema for the top-level report object and each section (`tasks`, `milestones`, `risks`, `dependencies`, and `next_week_priorities`) including required fields, data types, supported values for statuses/severity/priority, optional/default behavior, and example valid payloads. Update the existing schema-generation and validation tooling so the contract is represented consistently in code and documentation. (Custom Skill) — Approach 1

  Acceptance Criteria:
  - The repository contains one authoritative schema definition for the weekly status report input, including all required top-level fields and nested section structures.
  - The schema explicitly defines field names, types, mandatory vs optional fields, and supported enumerated values for statuses such as `Completed`, `In Progress`, `Blocked`, `Not Started`, and other relevant fields.
  - A valid example payload matching the schema is added or updated in the repo and can be used as the canonical sample for downstream generation and validation.
  - The existing schema-generation or validation tooling is updated so invalid or incomplete input produces clear, actionable errors instead of silent failures.
  - The project documentation includes a schema reference that explains the expected JSON structure and the meaning of each field for future implementation and QA.
- [ ] Define validation rules for missing required fields, malformed values, and unsupported statuses so the tool produces actionable errors instead of broken output (Custom Skill) — Approach 1
- [ ] Decide the output layout and file conventions for HTML and PDF artifacts, including default output names and directories (Custom Skill) — Approach 1
- [ ] Establish a local development workflow for running the CLI against sample data and reviewing generated artifacts (Custom Skill) — Approach 2

## Phase 2: Core Features

- [ ] Implement JSON input loading for the weekly status report, including robust file handling and clear exceptions for unreadable or invalid files (Custom Skill) — Approach 1
- [ ] Build the data validation layer to check the required report sections and enforce schema consistency before generation begins (Custom Skill) — Approach 2
- [ ] Add a normalized internal report model that converts raw JSON into a consistent structure for downstream rendering and aggregation (Custom Skill) — Approach 2
- [ ] Implement executive summary generation that captures the report headline, date, summary narrative, and a concise overview of this week’s progress (Custom Skill) — Approach 2
- [ ] Add task aggregation logic to calculate counts for Completed, In Progress, Blocked, and Not Started tasks (Custom Skill) — Approach 2
- [ ] Render the Current Work section with a table showing task ID, title, owner, priority, due date, status, and notes (Custom Skill) — Approach 2
- [ ] Add milestone rendering for milestone progress, target dates, status, and completion percentages (Custom Skill) — Approach 2
- [ ] Add explicit sections for risks, blockers, dependencies, and handoffs that make escalation items easy to spot (Custom Skill) — Approach 2
- [ ] Add next-week priorities rendering so the report closes with actionable follow-up items for the team and leadership (Custom Skill) — Approach 2
- [ ] Implement HTML report generation with executive-friendly layout, metric cards, clean sectioning, and readable styling (Custom Skill) — Approach 1
- [ ] Add PDF export support in the first release, including a configurable option to generate PDF alongside HTML when needed (Custom Skill) — Approach 1
- [ ] Build the command-line interface so a non-technical user can run the generator with a simple command and optional output arguments (Custom Skill) — Approach 1
- [ ] Add clear CLI help text, usage examples, and error messages for invalid arguments or input issues (Custom Skill) — Approach 1
- [ ] Ensure the current sample JSON file works end-to-end and produces a clean HTML report without additional coding (Custom Skill) — Approach 1

## Phase 3: Integration

- [ ] Introduce a future-ready data source abstraction so the JSON loader can be replaced or extended by API or database adapters without rewriting the reporting engine (Custom Skill) — Approach 1
- [ ] Define the common data contract that API/database-backed sources must satisfy before they can be rendered by the same report generation pipeline (Custom Skill) — Approach 1
- [ ] Add configuration hooks for recurring weekly report generation, including output path, input source selection, and optional PDF generation (Custom Skill) — Approach 1
- [ ] Design the loader/adapter boundary so the current JSON source remains the default while later phases can plug in external data sources (Custom Skill) — Approach 1
- [ ] Document the extension points for future API and database integrations so a technical owner can add new adapters with minimal rework (Custom Skill) — Approach 1
- [ ] Evaluate whether a lightweight settings/config file is needed for reusable command defaults and report generation options (Custom Skill) — Approach 1

## Phase 4: Testing

- [ ] Add unit tests for the JSON loader and input validation rules, including missing required fields and malformed JSON (Custom Skill) — Approach 2
- [ ] Add unit tests for status aggregation and summary calculations to verify counts and executive summary content (Custom Skill) — Approach 2
- [ ] Add rendering tests for HTML output structure, ensuring the required sections are present and correctly formatted (Custom Skill) — Approach 2
- [ ] Add PDF-generation tests that verify the export command completes successfully when configured and handles failures gracefully (Custom Skill) — Approach 2
- [ ] Add end-to-end tests that run the CLI with sample data and verify the generated HTML and PDF artifacts are created in the expected location (Custom Skill) — Approach 3
- [ ] Add regression tests for known edge cases such as empty task lists, missing optional fields, and unsupported task statuses (Custom Skill) — Approach 2
- [ ] Define a manual validation checklist for the Delivery Manager to confirm readability, content completeness, and executive suitability (Custom Skill) — Approach 1

## Phase 5: Documentation

- [ ] Update the main project README with setup steps, prerequisites, and a simple usage example for generating the weekly report (Custom Skill) — Approach 1
- [ ] Add a concise input schema reference showing the expected JSON structure for tasks, milestones, risks, dependencies, and next-week priorities (Custom Skill) — Approach 1
- [ ] Document the CLI commands, available flags, and default output behavior for non-technical users (Custom Skill) — Approach 1
- [ ] Add troubleshooting guidance for common issues, including invalid JSON, missing fields, and PDF export configuration problems (Custom Skill) — Approach 1
- [ ] Record the implementation approach and extension points for future API/database ingestion in the project docs (Custom Skill) — Approach 1
- [ ] Add a sample-generated HTML artifact and a sample PDF artifact (if supported) to demonstrate the expected output for stakeholders (Custom Skill) — Approach 3
- [ ] Capture the acceptance criteria and manual QA steps in the documentation so the team can verify the MVP before release (Custom Skill) — Approach 1

## Suggested Delivery Order

1. Setup and schema definition
2. JSON ingestion, validation, and HTML generation
3. PDF export and CLI polish
4. Integration abstraction for future data sources
5. Testing, QA, and documentation

## MVP Definition

The first release should be considered complete when all of the following are true:

- [ ] A user can generate a weekly status report from structured JSON input (Custom Skill) — Approach 1
- [ ] The report includes executive summary, task status, milestone status, risks, dependencies, and next-week priorities (Custom Skill) — Approach 2
- [ ] HTML output is generated successfully (Custom Skill) — Approach 1
- [ ] PDF output is available in the first release when configured (Custom Skill) — Approach 1
- [ ] The CLI is straightforward enough for a non-technical user to run (Custom Skill) — Approach 1
- [ ] Invalid or incomplete input produces clear, actionable error feedback (Custom Skill) — Approach 1

## Notes for Future Phases

- API-backed ingestion can be added after the JSON-based MVP is stable and validated
- Database-backed retrieval should follow the same normalized contract used by the JSON loader
- Additional reporting enhancements such as richer metrics, branding, and automated distribution can be deferred until after the core workflow is reliable
