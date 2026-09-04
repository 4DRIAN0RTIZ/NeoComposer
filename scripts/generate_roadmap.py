#!/usr/bin/env python3
"""Build docs/roadmap.json from GitHub issues labelled `roadmap`.

This is an OFFLINE FALLBACK generator. The docs site normally fetches issues
live at page load; this script only refreshes the static copy that is shown
when that fetch fails (offline, rate-limited, GitHub down).

Usage:
    python scripts/generate_roadmap.py [--repo OWNER/NAME]

Requires the `gh` CLI, authenticated. If `gh` is missing or the call fails the
script exits 0 and leaves docs/roadmap.json untouched.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "roadmap.json"

DEFAULT_REPO = "4DRIAN0RTIZ/NeoComposer"
DONE_WINDOW_DAYS = 60

# Static bilingual label map — kept in sync with the docs renderer.
LABELS = {
    "done": {"en": "✓ done", "es": "✓ hecho"},
    "planned": {"en": "planned", "es": "planeado"},
    "idea": {"en": "idea", "es": "idea"},
    "working": {"en": "in progress", "es": "en progreso"},
}

# Issue label -> roadmap status. Priority order matters (first match wins).
STATUS_LABELS = [
    ("roadmap:working", "working"),
    ("roadmap:planned", "planned"),
    ("roadmap:idea", "idea"),
]
STATUS_ORDER = ["working", "planned", "idea", "done"]

# Section titles for status-grouped (milestone-less) issues.
STATUS_SECTION_TITLES = {
    "working": {"en": "In progress", "es": "En progreso"},
    "planned": {"en": "Planned", "es": "Planeado"},
    "idea": {"en": "Ideas", "es": "Ideas"},
    "done": {"en": "Done", "es": "Hecho"},
}

_PREFIX_RE = re.compile(r"^\[roadmap\]\s*", re.IGNORECASE)


def _label_names(issue: dict) -> list[str]:
    return [lbl.get("name", "") for lbl in issue.get("labels") or []]


def resolve_status(issue: dict) -> str:
    if str(issue.get("state", "")).lower() == "closed":
        return "done"
    names = _label_names(issue)
    for label, status in STATUS_LABELS:
        if label in names:
            return status
    return "planned"


def strip_prefix(title: str) -> str:
    return _PREFIX_RE.sub("", title or "").strip()


def issue_to_item(issue: dict) -> dict:
    return {
        "status": resolve_status(issue),
        "text": strip_prefix(issue.get("title", "")),
        "ref": {
            "label": f"Issue #{issue.get('number')}",
            "url": issue.get("url", ""),
        },
    }


def _milestone_title(issue: dict) -> str | None:
    ms = issue.get("milestone")
    if not ms:
        return None
    title = ms.get("title")
    return title or None


def _milestone_due(issue: dict) -> str:
    ms = issue.get("milestone") or {}
    # Missing due date sorts last.
    return ms.get("dueOn") or ms.get("due_on") or "9999-12-31T00:00:00Z"


def _within_done_window(issue: dict) -> bool:
    closed = issue.get("closedAt") or issue.get("updatedAt")
    if not closed:
        return False
    try:
        when = datetime.fromisoformat(str(closed).replace("Z", "+00:00"))
    except ValueError:
        return False
    return datetime.now(timezone.utc) - when <= timedelta(days=DONE_WINDOW_DAYS)


def _sort_items(items: list[dict]) -> list[dict]:
    return sorted(
        items,
        key=lambda it: (
            STATUS_ORDER.index(it["status"]) if it["status"] in STATUS_ORDER else 99,
            it["_updatedAt"],
        ),
    )


def build_sections(issues: list[dict]) -> list[dict]:
    roadmap_issues = [i for i in issues if "roadmap" in _label_names(i)]

    milestone_groups: dict[str, dict] = {}
    status_groups: dict[str, list[dict]] = {}

    for issue in roadmap_issues:
        status = resolve_status(issue)
        milestone = _milestone_title(issue)

        # Drop stale done items only when they have no milestone; milestone
        # sections keep their history (they represent shipped versions).
        if status == "done" and not milestone and not _within_done_window(issue):
            continue

        item = issue_to_item(issue)
        item["_updatedAt"] = issue.get("updatedAt", "")

        if milestone:
            group = milestone_groups.setdefault(
                milestone, {"title": milestone, "due": _milestone_due(issue), "items": []}
            )
            group["items"].append(item)
        else:
            status_groups.setdefault(status, []).append(item)

    sections: list[dict] = []

    for group in sorted(milestone_groups.values(), key=lambda g: (g["due"], g["title"])):
        sections.append(
            {
                "title": group["title"],
                "items": [_strip_internal(it) for it in _sort_items(group["items"])],
            }
        )

    for status in STATUS_ORDER:
        items = status_groups.get(status)
        if not items:
            continue
        sections.append(
            {
                "title": STATUS_SECTION_TITLES[status],
                "items": [_strip_internal(it) for it in _sort_items(items)],
            }
        )

    return sections


def _strip_internal(item: dict) -> dict:
    return {k: v for k, v in item.items() if not k.startswith("_")}


def build_roadmap(issues: list[dict]) -> dict:
    return {"labels": LABELS, "sections": build_sections(issues)}


def fetch_issues(repo: str) -> list[dict] | None:
    try:
        subprocess.run(["gh", "--version"], check=True, capture_output=True)
    except (OSError, subprocess.CalledProcessError):
        print("generate_roadmap: gh not available, keeping docs/roadmap.json", file=sys.stderr)
        return None
    try:
        raw = subprocess.run(
            [
                "gh", "issue", "list",
                "--repo", repo,
                "--label", "roadmap",
                "--state", "all",
                "--limit", "200",
                "--json", "number,title,body,state,labels,assignees,milestone,updatedAt,closedAt,url",
            ],
            check=True,
            capture_output=True,
            text=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        print("generate_roadmap: gh issue list failed, keeping docs/roadmap.json", file=sys.stderr)
        return None
    parsed = json.loads(raw)
    return parsed if isinstance(parsed, list) else []


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=DEFAULT_REPO, help="OWNER/NAME (default: %(default)s)")
    args = parser.parse_args(argv)

    issues = fetch_issues(args.repo)
    if issues is None:
        return 0

    roadmap = build_roadmap(issues)
    OUT.write_text(json.dumps(roadmap, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"generate_roadmap: wrote {OUT.relative_to(ROOT)} ({len(roadmap['sections'])} sections)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
