#!/usr/bin/env python3
"""Bulk markdown validation helper.

This simple script discovers candidate files in a target directory, builds an
instruction prompt for each file, optionally sends that prompt to an AI CLI,
and writes the responses to a JSON output file.

Example usage:
    python validationrules.py --target-dir . --pattern "*.md" --output-file results.json
    python validationrules.py --target-dir . --pattern "*.md" --output-file results.json --ai-mode command --ai-executable "copilot"
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

DEFAULT_INSTRUCTION = (
    "Review the provided Markdown file for consistent formatting. "
    "Check heading hierarchy, bullet indentation, spacing around code fences, "
    "and obvious whitespace issues. Return a concise result that reports if the "
    "file is clean or lists the specific issues that need attention."
)


def discover_files(target_dir: Path, pattern: str, max_files: int | None) -> list[Path]:
    files = sorted(target_dir.rglob(pattern))
    files = [file for file in files if file.is_file()]
    if max_files is not None:
        files = files[:max_files]
    return files


def build_prompt(file_path: Path, file_text: str, instruction: str) -> str:
    return (
        "Instruction:\n"
        f"{instruction}\n\n"
        "Target file:\n"
        f"{file_path}\n\n"
        "File contents:\n"
        f"{file_text}\n"
    )


def invoke_local_ai(prompt: str) -> str:
    lines = prompt.strip().splitlines()
    file_name = lines[2] if len(lines) > 2 else "unknown file"
    file_text = prompt.split("File contents:\n", 1)[1].strip()

    issues = []
    if file_text.rstrip() != file_text:
        issues.append("Trailing whitespace detected.")
    if file_text.count("```") % 2 != 0:
        issues.append("Unbalanced fenced code blocks detected.")

    headings = []
    for idx, line in enumerate(file_text.splitlines(), 1):
        if line.startswith("#"):
            headings.append((idx, len(line) - len(line.lstrip("#"))))

    prev_level = 0
    for line_no, level in headings:
        if prev_level and level > prev_level + 1:
            issues.append(
                f"Heading jump detected at line {line_no}: H{prev_level} -> H{level}."
            )
            break
        prev_level = level

    if issues:
        return (
            f"AI review for {file_name}:\n"
            + "\n".join(f"- {issue}" for issue in issues)
        )

    return f"AI review for {file_name}:\n- No formatting issues detected."


def invoke_command_ai(prompt: str, executable: str) -> str:
    result = subprocess.run(
        [executable],
        input=prompt,
        text=True,
        capture_output=True,
        check=False,
    )

    if result.returncode != 0:
        stderr = result.stderr.strip() or "unknown error"
        raise RuntimeError(f"AI command failed with exit code {result.returncode}: {stderr}")

    return (result.stdout or result.stderr).strip()


def write_output(results: list[dict], output_file: Path) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(json.dumps(results, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Discover target files, build AI prompts, and save results to an output file."
    )
    parser.add_argument(
        "--target-dir",
        default=".",
        help="Directory to scan for target files (default: current directory).",
    )
    parser.add_argument(
        "--pattern",
        default="*.md",
        help="Glob pattern used to discover files (default: *.md).",
    )
    parser.add_argument(
        "--output-file",
        default="validationrules-output.json",
        help="File path where the results should be written.",
    )
    parser.add_argument(
        "--instruction",
        default=DEFAULT_INSTRUCTION,
        help="Instruction text included in the prompt sent to the AI for each file.",
    )
    parser.add_argument(
        "--max-files",
        type=int,
        default=None,
        help="Optional limit on how many matching files are processed.",
    )
    parser.add_argument(
        "--ai-mode",
        choices=["local", "command"],
        default="local",
        help="Use a local simulator or an external command for the AI step.",
    )
    parser.add_argument(
        "--ai-executable",
        default="",
        help="Executable used when --ai-mode command is selected.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    target_dir = Path(args.target_dir).resolve()
    output_file = Path(args.output_file)

    if not target_dir.exists():
        print(f"Target directory not found: {target_dir}", file=sys.stderr)
        return 1

    files = discover_files(target_dir, args.pattern, args.max_files)
    if not files:
        print(f"No files matched pattern '{args.pattern}' under {target_dir}", file=sys.stderr)
        return 1

    results: list[dict] = []

    for file_path in files:
        file_text = file_path.read_text(encoding="utf-8")
        prompt = build_prompt(file_path, file_text, args.instruction)

        if args.ai_mode == "command":
            if not args.ai_executable:
                print("--ai-executable is required when --ai-mode command is selected.", file=sys.stderr)
                return 1
            try:
                response = invoke_command_ai(prompt, args.ai_executable)
            except Exception as exc:
                print(f"Error processing {file_path}: {exc}", file=sys.stderr)
                return 1
        else:
            response = invoke_local_ai(prompt)

        results.append(
            {
                "file": str(file_path),
                "result": response,
            }
        )

    write_output(results, output_file)

    print(f"Processed {len(results)} file(s). Results saved to {output_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
