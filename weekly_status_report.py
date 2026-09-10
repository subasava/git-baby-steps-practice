#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from html import escape


def load_data(input_path: str):
    with open(input_path, "r", encoding="utf-8") as f:
        return json.load(f)


def status_counts(tasks):
    counts = {"Completed": 0, "In Progress": 0, "Blocked": 0, "Not Started": 0}
    for task in tasks:
        status = task.get("status", "Not Started")
        if status in counts:
            counts[status] += 1
        else:
            counts["Not Started"] += 1
    return counts


def render_task_rows(tasks):
    if not tasks:
        return "<p>No task tracker updates were provided for this week.</p>"

    rows = []
    for task in tasks:
        task_id = escape(task.get("id", "-"))
        title = escape(task.get("title", "Untitled task"))
        status = escape(task.get("status", "Not Started"))
        owner = escape(task.get("owner", "Unassigned"))
        priority = escape(task.get("priority", "Normal"))
        due = escape(task.get("due", "TBD"))
        note = escape(task.get("note", ""))

        rows.append(
            f"""
            <tr>
                <td>{task_id}</td>
                <td>{title}</td>
                <td>{status}</td>
                <td>{owner}</td>
                <td>{priority}</td>
                <td>{due}</td>
                <td>{note}</td>
            </tr>
            """
        )

    return f"""
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Task</th>
                <th>Status</th>
                <th>Owner</th>
                <th>Priority</th>
                <th>Due</th>
                <th>Notes</th>
            </tr>
        </thead>
        <tbody>
            {''.join(rows)}
        </tbody>
    </table>
    """


def render_risks(risks):
    if not risks:
        return ""

    risk_items = "".join(f"<li>{escape(item)}</li>" for item in risks)
    return f"""
    <section>
        <h2>Risks & Dependencies</h2>
        <ul>
            {risk_items}
        </ul>
    </section>
    """


def render_next_week_priorities(next_week_priorities):
    if not next_week_priorities:
        return ""

    items = "".join(f"<li>{escape(item)}</li>" for item in next_week_priorities)
    return f"""
    <section>
        <h2>Next Week's Priorities</h2>
        <ul>
            {items}
        </ul>
    </section>
    """


def render_html(report_data):
    headline = escape(report_data.get("headline", "Weekly Status Report"))
    report_date = escape(report_data.get("report_date", ""))
    summary = escape(report_data.get("summary", ""))
    tasks = report_data.get("tasks", [])
    counts = status_counts(tasks)

    task_table = render_task_rows(tasks)
    risks_section = render_risks(report_data.get("risks", []))
    priorities_section = render_next_week_priorities(report_data.get("next_week_priorities", []))

    metrics = f"""
    <div class="metrics">
        <div class="metric">
            <span class="label">Completed</span>
            <span class="value">{counts['Completed']}</span>
        </div>
        <div class="metric">
            <span class="label">In Progress</span>
            <span class="value">{counts['In Progress']}</span>
        </div>
        <div class="metric">
            <span class="label">Blocked</span>
            <span class="value">{counts['Blocked']}</span>
        </div>
        <div class="metric">
            <span class="label">Not Started</span>
            <span class="value">{counts['Not Started']}</span>
        </div>
    </div>
    """

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>{headline}</title>
        <style>
            body {{
                font-family: Arial, Helvetica, sans-serif;
                margin: 0;
                background: #f5f7fb;
                color: #1f2937;
            }}
            .email-wrapper {{
                max-width: 900px;
                margin: 32px auto;
                background: #ffffff;
                border: 1px solid #dfe3ea;
                border-radius: 10px;
                overflow: hidden;
            }}
            .header {{
                background: #0f172a;
                color: #ffffff;
                padding: 24px;
            }}
            .header h1 {{
                margin: 0;
                font-size: 28px;
            }}
            .header .date {{
                margin-top: 8px;
                color: #cbd5e1;
                font-size: 14px;
            }}
            .content {{
                padding: 24px;
            }}
            .summary {{
                margin-bottom: 24px;
                padding: 16px;
                border-left: 4px solid #3b82f6;
                background: #eff6ff;
                border-radius: 6px;
            }}
            .metrics {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
                gap: 12px;
                margin-bottom: 24px;
            }}
            .metric {{
                background: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 16px;
            }}
            .metric .label {{
                display: block;
                color: #475569;
                font-size: 12px;
                text-transform: uppercase;
                letter-spacing: 0.04em;
                margin-bottom: 8px;
            }}
            .metric .value {{
                font-size: 24px;
                font-weight: 700;
            }}
            h2 {{
                font-size: 20px;
                margin-top: 24px;
                margin-bottom: 12px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                font-size: 14px;
            }}
            th, td {{
                padding: 12px;
                border-bottom: 1px solid #e2e8f0;
                text-align: left;
                vertical-align: top;
            }}
            th {{
                background: #f8fafc;
                font-weight: 700;
            }}
            ul {{
                margin-top: 0;
                padding-left: 18px;
            }}
            li {{
                margin-bottom: 8px;
            }}
            .footer {{
                padding: 16px 24px 24px;
                font-size: 12px;
                color: #64748b;
            }}
        </style>
    </head>
    <body>
        <div class="email-wrapper">
            <div class="header">
                <h1>{headline}</h1>
                <div class="date">{report_date}</div>
            </div>
            <div class="content">
                <div class="summary">{summary}</div>
                {metrics}
                <section>
                    <h2>Current Work</h2>
                    {task_table}
                </section>
                {risks_section}
                {priorities_section}
            </div>
            <div class="footer">
                Generated automatically from task tracker input.
            </div>
        </div>
    </body>
    </html>
    """


def build_report(input_path: str, output_path: str):
    report_data = load_data(input_path)
    html_content = render_html(report_data)

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html_content, encoding="utf-8")

    print(f"Report generated successfully: {output}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate an email-ready HTML weekly status report from task tracker data."
    )
    parser.add_argument("input", help="Path to a JSON file containing task tracker data.")
    parser.add_argument(
        "-o",
        "--output",
        default="weekly_status_report.html",
        help="Output path for the generated HTML file.",
    )
    args = parser.parse_args()

    build_report(args.input, args.output)


if __name__ == "__main__":
    main()
