#!/usr/bin/env python3
"""Build a report input schema from command-line arguments.

This script accepts the core report fields needed by the weekly status report
input schema and emits a JSON object that can be saved to a file or piped into
another process.

Example:
    python tools/reportinputschema.py \
        --headline "Weekly Status Report" \
        --report-date "September 10, 2026" \
        --summary "Weekly summary" \
        --tasks '[{"id":"TASK-101","title":"Finalize sprint planning","status":"Completed","owner":"Alex","priority":"High","due":"2026-09-08","note":"Planning completed."}]' \
        --milestones '[{"id":"MS-01","name":"Migration phase 1","status":"On Track","target_date":"2026-09-30","completion_percent":65}]' \
        --risks '["Partner team response is pending."]' \
        --dependencies '[{"id":"DEP-01","description":"External API dependency","owner":"Priya","status":"Blocked","action_required":"Confirm partner response."}]' \
        --next-week-priorities '["Resolve dependency with partner team."]'
"""

import argparse
import json
import sys
from typing import Any


def parse_json_argument(value: str, field_name: str) -> Any:
    """Parse a CLI JSON argument for a field such as tasks or milestones."""
    try:
        return json.loads(value)
    except json.JSONDecodeError as exc:
        raise SystemExit(
            f"Invalid JSON for {field_name}: {value!r}. Error: {exc.msg}"
        ) from exc


def parse_optional_json_argument(value: str | None, field_name: str) -> Any:
    if value is None:
        return []
    return parse_json_argument(value, field_name)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build a weekly report input schema JSON payload from command-line arguments."
    )

    parser.add_argument(
        "--headline",
        default="Weekly Status Report",
        help="Headline for the report (default: Weekly Status Report)",
    )
    parser.add_argument(
        "--report-date",
        default="",
        help="Report date string (optional)",
    )
    parser.add_argument(
        "--summary",
        default="",
        help="High-level summary text (optional)",
    )
    parser.add_argument(
        "--tasks",
        required=True,
        help='JSON array of tasks. Example: \'[{"id":"TASK-101", "title":"Task", "status":"Completed", "owner":"Alex", "priority":"High", "due":"2026-09-15", "note":"Notes"}]\'',
    )
    parser.add_argument(
        "--milestones",
        required=True,
        help='JSON array of milestones. Example: \'[{"id":"MS-01", "name":"Migration phase 1", "status":"On Track", "target_date":"2026-09-30", "completion_percent":65}]\'',
    )
    parser.add_argument(
        "--risks",
        help="JSON array of risks or strings. Optional.",
    )
    parser.add_argument(
        "--dependencies",
        help="JSON array of dependencies. Optional.",
    )
    parser.add_argument(
        "--next-week-priorities",
        help="JSON array of next week priorities. Optional.",
    )

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    report = {
        "headline": args.headline,
        "report_date": args.report_date,
        "summary": args.summary,
        "tasks": parse_json_argument(args.tasks, "tasks"),
        "milestones": parse_json_argument(args.milestones, "milestones"),
        "risks": parse_optional_json_argument(args.risks, "risks"),
        "dependencies": parse_optional_json_argument(args.dependencies, "dependencies"),
        "next_week_priorities": parse_optional_json_argument(
            args.next_week_priorities, "next_week_priorities"
        ),
    }

    # Ensure the required top-level structure is JSON-serializable.
    json.dump(report, sys.stdout, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
