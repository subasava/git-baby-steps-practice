# Use Validate Report Data Tool

Use this instruction when the user needs to validate a specific section of a weekly status report JSON payload.

When to use the tool:
- The user wants to confirm that `tasks`, `milestones`, `risks`, `dependencies`, or `next_week_priorities` match the expected schema.
- The user has a report payload and wants to check whether a particular section is structurally valid.
- The user wants to verify the input before passing it to other tools or generating a report.

Tool to use:
- `tools/validatereportdata.py`

How to invoke it:
- Run:
  `python tools/validatereportdata.py <section> --file <report-json-file>`
- Or pass inline JSON:
  `python tools/validatereportdata.py <section> --data '<json payload>'`
- Or pipe JSON via stdin.

Valid section names:
- `tasks`
- `milestones`
- `risks`
- `dependencies`
- `next_week_priorities`

Examples:
- `python tools/validatereportdata.py tasks --file sample_weekly_report.json`
- `python tools/validatereportdata.py milestones --data '{"milestones": [{"id": "MS-01", "name": "Migration phase 1", "status": "On Track", "target_date": "2026-09-30", "completion_percent": 65}]}'`

How to present results:
- Report whether the selected section is valid.
- If the section is invalid, explain the specific schema issue that was detected.
- Keep the response concise and focused on validation outcome.
