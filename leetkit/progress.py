"""progress.json: every time you solved a problem.

    {"two-sum": {"solves": ["2026-09-21", "2026-09-25"], "code": "<hash of the solution last Accepted>", "reset": false}}

`leet list` shows them as the strokes of 正, one per solve, up to the full five. An Accepted run is a new solve when it
is the first one ever, the first one since `leet reset`, or the first one on a new day with different code. Checking
the same solution again never adds a stroke.

Like journal.jsonl the file is yours, not the repo's: git ignores it. (Before strokes it held one date per problem,
"two-sum": "2026-09-21"; that reads as a single solve.)
"""

from __future__ import annotations

import json
from datetime import date

from .catalog import ROOT

PATH = ROOT / "progress.json"


def _read() -> dict[str, dict]:
    try:
        raw = json.loads(PATH.read_text())
    except (OSError, ValueError):
        return {}
    return {slug: entry if isinstance(entry, dict) else {"solves": [entry], "code": None, "reset": False}
            for slug, entry in raw.items()}


def _write(entries: dict[str, dict]) -> None:
    try:
        PATH.write_text(json.dumps(entries, indent=2, sort_keys=True) + "\n")
    except OSError:
        pass


def solves() -> dict[str, int]:
    """How many times each problem has been solved; problems never solved are not in it."""
    return {slug: len(entry["solves"]) for slug, entry in _read().items() if entry.get("solves")}


def mark_solved(slug: str, code: str = "") -> bool:
    """Called on every Accepted. True when this one counted as a new solve."""
    entries = _read()
    entry = entries.setdefault(slug, {"solves": [], "code": None, "reset": False})
    today = date.today().isoformat()
    # A mark carried over from the older file has no code on record: the first Accepted only puts it on record.
    again = bool(entry["solves"]) and not entry.get("reset") and (
        entry["solves"][-1] == today or entry.get("code") in (code, None))
    if not again:
        entry["solves"].append(today)
        entry["reset"] = False
    if not again or entry.get("code") != code:
        entry["code"] = code                                # the code last Accepted: coming back to it tomorrow is no new solve
        _write(entries)
    return not again


def note_reset(slug: str) -> None:
    """The solution went back to empty: the next Accepted is a solve of its own."""
    entries = _read()
    if slug in entries:
        entries[slug]["reset"] = True
        _write(entries)


def forget_all() -> None:
    PATH.unlink(missing_ok=True)
