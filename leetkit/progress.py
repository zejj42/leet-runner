"""progress.json: the problems you have solved, and the day each was first Accepted.

    {"two-sum": "2026-09-21"}

Like journal.jsonl it is yours, not the repo's: git ignores it. Solved stays solved, as on LeetCode, whatever a
later run says.
"""

from __future__ import annotations

import json
from datetime import date

from .catalog import ROOT

PATH = ROOT / "progress.json"


def solved() -> dict[str, str]:
    try:
        return json.loads(PATH.read_text())
    except (OSError, ValueError):
        return {}


def mark_solved(slug: str) -> None:
    known = solved()
    if slug in known:
        return
    known[slug] = date.today().isoformat()
    try:
        PATH.write_text(json.dumps(known, indent=2, sort_keys=True) + "\n")
    except OSError:
        pass
