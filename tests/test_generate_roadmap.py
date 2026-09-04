"""Tests for scripts/generate_roadmap.py — the issue-driven roadmap builder."""

import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import generate_roadmap as gr  # noqa: E402


def _iso(days_ago: int) -> str:
    return (datetime.now(timezone.utc) - timedelta(days=days_ago)).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )


def issue(**kw):
    """Build a gh-issue-list-style dict with sensible defaults."""
    number = kw.get("number", 1)
    base = {
        "number": number,
        "title": "[roadmap] Example",
        "body": "",
        "state": "OPEN",
        "labels": [{"name": "roadmap"}],
        "assignees": [],
        "milestone": None,
        "updatedAt": _iso(1),
        "closedAt": None,
        "url": f"https://github.com/4DRIAN0RTIZ/NeoComposer/issues/{number}",
    }
    base.update(kw)
    return base


class TestResolveStatus:
    def test_closed_issue_is_done(self):
        assert gr.resolve_status(issue(state="CLOSED")) == "done"

    def test_working_label(self):
        i = issue(labels=[{"name": "roadmap"}, {"name": "roadmap:working"}])
        assert gr.resolve_status(i) == "working"

    def test_idea_label(self):
        i = issue(labels=[{"name": "roadmap"}, {"name": "roadmap:idea"}])
        assert gr.resolve_status(i) == "idea"

    def test_no_status_label_defaults_to_planned(self):
        assert gr.resolve_status(issue()) == "planned"

    def test_working_wins_over_planned(self):
        i = issue(
            labels=[
                {"name": "roadmap"},
                {"name": "roadmap:planned"},
                {"name": "roadmap:working"},
            ]
        )
        assert gr.resolve_status(i) == "working"

    def test_closed_wins_over_status_label(self):
        i = issue(state="CLOSED", labels=[{"name": "roadmap"}, {"name": "roadmap:working"}])
        assert gr.resolve_status(i) == "done"


class TestStripPrefix:
    def test_strips_bracket_prefix_with_space(self):
        assert gr.strip_prefix("[roadmap] Multi-account support") == "Multi-account support"

    def test_strips_bracket_prefix_without_space(self):
        assert gr.strip_prefix("[roadmap]Multi-account") == "Multi-account"

    def test_case_insensitive(self):
        assert gr.strip_prefix("[Roadmap] Thing") == "Thing"

    def test_leaves_untouched_when_no_prefix(self):
        assert gr.strip_prefix("Plain title") == "Plain title"


class TestIssueToItem:
    def test_shape(self):
        i = issue(number=12, title="[roadmap] Sent email history")
        item = gr.issue_to_item(i)
        assert item == {
            "status": "planned",
            "text": "Sent email history",
            "ref": {
                "label": "Issue #12",
                "url": "https://github.com/4DRIAN0RTIZ/NeoComposer/issues/12",
            },
        }


class TestBuildSections:
    def test_milestone_issues_grouped_by_milestone_title(self):
        issues = [
            issue(number=1, title="[roadmap] A", milestone={"title": "v2.0.0", "dueOn": None}),
            issue(number=2, title="[roadmap] B", milestone={"title": "v2.0.0", "dueOn": None}),
        ]
        sections = gr.build_sections(issues)
        assert [s["title"] for s in sections] == ["v2.0.0"]
        assert [it["text"] for it in sections[0]["items"]] == ["A", "B"]

    def test_milestone_sections_ordered_by_due_date_then_title(self):
        issues = [
            issue(number=1, title="[roadmap] A", milestone={"title": "v3.0.0", "dueOn": _iso(-60)}),
            issue(number=2, title="[roadmap] B", milestone={"title": "v2.0.0", "dueOn": _iso(-30)}),
            issue(number=3, title="[roadmap] C", milestone={"title": "backlog", "dueOn": None}),
        ]
        titles = [s["title"] for s in gr.build_sections(issues)]
        assert titles == ["v2.0.0", "v3.0.0", "backlog"]

    def test_milestoneless_issues_grouped_by_status(self):
        issues = [
            issue(number=1, title="[roadmap] W", labels=[{"name": "roadmap"}, {"name": "roadmap:working"}]),
            issue(number=2, title="[roadmap] P"),
            issue(number=3, title="[roadmap] I", labels=[{"name": "roadmap"}, {"name": "roadmap:idea"}]),
        ]
        sections = gr.build_sections(issues)
        titles = [s["title"]["en"] if isinstance(s["title"], dict) else s["title"] for s in sections]
        assert titles == ["In progress", "Planned", "Ideas"]

    def test_milestone_sections_come_before_status_sections(self):
        issues = [
            issue(number=1, title="[roadmap] S"),  # milestoneless -> status
            issue(number=2, title="[roadmap] M", milestone={"title": "v2.0.0", "dueOn": None}),
        ]
        titles = [s["title"] for s in gr.build_sections(issues)]
        assert titles[0] == "v2.0.0"

    def test_empty_status_groups_are_omitted(self):
        issues = [issue(number=1, title="[roadmap] only planned")]
        sections = gr.build_sections(issues)
        assert len(sections) == 1

    def test_old_milestoneless_done_item_is_dropped(self):
        issues = [
            issue(
                number=1,
                title="[roadmap] ancient",
                state="CLOSED",
                closedAt=_iso(120),
                updatedAt=_iso(120),
            )
        ]
        assert gr.build_sections(issues) == []

    def test_old_done_item_kept_when_it_has_a_milestone(self):
        issues = [
            issue(
                number=1,
                title="[roadmap] shipped in v0.1.0",
                state="CLOSED",
                closedAt=_iso(120),
                updatedAt=_iso(120),
                milestone={"title": "v0.1.0", "dueOn": _iso(115)},
            )
        ]
        sections = gr.build_sections(issues)
        assert [s["title"] for s in sections] == ["v0.1.0"]


class TestBuildRoadmap:
    def test_includes_static_label_map_and_sections(self):
        roadmap = gr.build_roadmap([issue(number=1, title="[roadmap] X")])
        assert set(roadmap["labels"]) == {"done", "planned", "idea", "working"}
        assert roadmap["labels"]["done"] == {"en": "✓ done", "es": "✓ hecho"}
        assert isinstance(roadmap["sections"], list)

    def test_non_roadmap_issues_are_ignored(self):
        issues = [
            issue(number=1, title="[roadmap] keep"),
            issue(number=2, title="unrelated", labels=[{"name": "bug"}]),
        ]
        roadmap = gr.build_roadmap(issues)
        all_texts = [it["text"] for s in roadmap["sections"] for it in s["items"]]
        assert all_texts == ["keep"]
