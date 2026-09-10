from weekly_status_report import render_html, status_counts


def test_status_counts_groups_known_statuses_and_falls_back_for_unknown_values():
    tasks = [
        {"status": "Completed"},
        {"status": "In Progress"},
        {"status": "Blocked"},
        {"status": "Pending Approval"},
        {"status": "Not Started"},
        {"status": "Unknown Status"},
        {},
    ]

    assert status_counts(tasks) == {
        "Completed": 1,
        "In Progress": 1,
        "Blocked": 1,
        "Pending Approval": 1,
        "Not Started": 3,
    }


def test_render_html_includes_report_metadata_summary_and_metric_values():
    report_data = {
        "headline": "Weekly Status Report",
        "report_date": "September 10, 2026",
        "summary": "This week, the team delivered core work items and kept momentum on in-progress initiatives.",
        "tasks": [
            {"id": "TASK-101", "title": "Finalize sprint planning", "status": "Completed", "owner": "Alex", "priority": "High", "due": "2026-09-08", "note": "Approved by leadership."},
            {"id": "TASK-102", "title": "Implement weekly stakeholder update workflow", "status": "In Progress", "owner": "Jordan", "priority": "High", "due": "2026-09-15", "note": "Automation script is in place."},
            {"id": "TASK-103", "title": "Review dependency on external API", "status": "Blocked", "owner": "Priya", "priority": "Medium", "due": "2026-09-12", "note": "Waiting on partner team."},
            {"id": "TASK-104", "title": "Prepare onboarding checklist", "status": "Pending Approval", "owner": "Sam", "priority": "Low", "due": "2026-09-18", "note": "Needs business approval before kickoff."},
            {"id": "TASK-105", "title": "Refresh onboarding checklist", "status": "Not Started", "owner": "Sam", "priority": "Low", "due": "2026-09-18", "note": "Needs final review."},
        ],
    }

    html = render_html(report_data)

    assert "Weekly Status Report" in html
    assert "September 10, 2026" in html
    assert "This week, the team delivered core work items and kept momentum on in-progress initiatives." in html
    assert 'class="summary"' in html
    assert 'Completed</span>\n            <span class="value">1</span>' in html
    assert 'In Progress</span>\n            <span class="value">1</span>' in html
    assert 'Blocked</span>\n            <span class="value">1</span>' in html
    assert 'Pending Approval</span>\n            <span class="value">1</span>' in html
    assert 'Not Started</span>\n            <span class="value">1</span>' in html
    assert "TASK-101" in html
    assert "Current Work" in html


def test_render_html_handles_empty_tasks_without_breaking_summary_generation():
    report_data = {
        "headline": "Weekly Status Report",
        "report_date": "September 10, 2026",
        "summary": "The team is starting this week with no tracked tasks yet.",
        "tasks": [],
    }

    html = render_html(report_data)

    assert "No task tracker updates were provided for this week." in html
    assert "The team is starting this week with no tracked tasks yet." in html
    assert 'Completed</span>\n            <span class="value">0</span>' in html
    assert 'In Progress</span>\n            <span class="value">0</span>' in html
    assert 'Blocked</span>\n            <span class="value">0</span>' in html
    assert 'Pending Approval</span>\n            <span class="value">0</span>' in html
    assert 'Not Started</span>\n            <span class="value">0</span>' in html
