#!/usr/bin/env python3
"""Validate a named report section against the expected schema.

Usage examples:
    python tools/validatereportdata.py tasks --file sample_weekly_report.json
    python tools/validatereportdata.py milestones --file sample_weekly_report.json
    python tools/validatereportdata.py risks --file sample_weekly_report.json

The script accepts a report section name (for example: tasks, milestones,
risks, dependencies, next_week_priorities) and validates that section in the
provided JSON payload.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any

VALID_SECTIONS = {
    "tasks": "tasks",
    "milestones": "milestones",
    "risks": "risks",
    "dependencies": "dependencies",
    "next_week_priorities": "next_week_priorities",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a named report section from a JSON report payload."
    )
    parser.add_argument(
        "section",
        choices=sorted(VALID_SECTIONS),
        help=(
            "Section name to validate: tasks, milestones, risks, dependencies, "
            "or next_week_priorities"
        ),
    )
    parser.add_argument(
        "--file",
        "-f",
        help="Path to a JSON report file. If omitted, the script reads from stdin.",
    )
    parser.add_argument(
        "--data",
        "-d",
        help="Inline JSON string to validate instead of reading from a file or stdin.",
    )
    return parser.parse_args()


def load_payload(args: argparse.Namespace) -> Any:
    if args.data is not None:
        try:
            return json.loads(args.data)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"Invalid JSON provided via --data: {exc}") from exc

    if args.file:
        try:
            raw_text = Path(args.file).read_text(encoding="utf-8")
        except OSError as exc:
            raise SystemExit(f"Failed to read file '{args.file}': {exc}") from exc
        try:
            return json.loads(raw_text)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"Invalid JSON in '{args.file}': {exc}") from exc

    raw_text = sys.stdin.read()
    if not raw_text.strip():
        raise SystemExit("No input provided. Pass --file, --data, or pipe JSON via stdin.")

    try:
        return json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON from stdin: {exc}") from exc


def require_object(item: Any, section: str, index: int | None = None) -> dict:
    if not isinstance(item, dict):
        location = f" at index {index}" if index is not None else ""
        raise SystemExit(
            f"Invalid {section} entry{location}: expected an object, got {type(item).__name__}"
        )
    return item


def validate_tasks(tasks: Any) -> None:
    if not isinstance(tasks, list):
        raise SystemExit(f"Invalid tasks section: expected a list, got {type(tasks).__name__}")

    required_fields = ["id", "title", "status", "owner", "priority", "due", "note"]
    for index, task in enumerate(tasks):
        task_obj = require_object(task, "tasks", index)
        missing = [field for field in required_fields if field not in task_obj]
        if missing:
            raise SystemExit(
                f"Invalid tasks entry at index {index}: missing required fields: {', '.join(missing)}"
            )


def validate_milestones(milestones: Any) -> None:
    if not isinstance(milestones, list):
        raise SystemExit(
            f"Invalid milestones section: expected a list, got {type(milestones).__name__}"
        )

    required_fields = ["id", "name", "status", "target_date", "completion_percent"]
    for index, milestone in enumerate(milestones):
        milestone_obj = require_object(milestone, "milestones", index)
        missing = [field for field in required_fields if field not in milestone_obj]
        if missing:
            raise SystemExit(
                f"Invalid milestones entry at index {index}: missing required fields: {', '.join(missing)}"
            )


def validate_risks(risks: Any) -> None:
    if not isinstance(risks, list):
        raise SystemExit(
            f"Invalid risks section: expected a list, got {type(risks).__name__}"
        )

    for index, risk in enumerate(risks):
        if isinstance(risk, str):
            continue
        risk_obj = require_object(risk, "risks", index)
        if "description" not in risk_obj:
            raise SystemExit(
                f"Invalid risks entry at index {index}: missing required field 'description'"
            )


def validate_dependencies(dependencies: Any) -> None:
    if not isinstance(dependencies, list):
        raise SystemExit(
            f"Invalid dependencies section: expected a list, got {type(dependencies).__name__}"
        )

    required_fields = ["id", "description", "owner", "status", "action_required"]
    for index, dependency in enumerate(dependencies):
        dependency_obj = require_object(dependency, "dependencies", index)
        missing = [field for field in required_fields if field not in dependency_obj]
        if missing:
            raise SystemExit(
                f"Invalid dependencies entry at index {index}: missing required fields: {', '.join(missing)}"
            )


def validate_next_week_priorities(next_week_priorities: Any) -> None:
    if not isinstance(next_week_priorities, list):
        raise SystemExit(
            f"Invalid next_week_priorities section: expected a list, got {type(next_week_priorities).__name__}"
        )

    for index, item in enumerate(next_week_priorities):
        if not isinstance(item, str):
            raise SystemExit(
                f"Invalid next_week_priorities entry at index {index}: expected a string, got {type(item).__name__}"
            )


SECTION_VALIDATORS = {
    "tasks": validate_tasks,
    "milestones": validate_milestones,
    "risks": validate_risks,
    "dependencies": validate_dependencies,
    "next_week_priorities": validate_next_week_priorities,
}


def validate_section(payload: Any, section: str) -> None:
    if not isinstance(payload, dict):
        raise SystemExit(
            f"Invalid report payload: expected a JSON object, got {type(payload).__name__}"
        )

    if section not in payload:
        raise SystemExit(
            f"Invalid report payload: missing required section '{section}'"
        )

    validator = SECTION_VALIDATORS[section]
    validator(payload[section])


def main() -> None:
    args = parse_args()
    payload = load_payload(args)
    validate_section(payload, args.section)

    print(f"Section '{args.section}' is valid.")


if __name__ == "__main__":
    main()
