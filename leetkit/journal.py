"""journal.jsonl: one line for every time `leet` is run, whatever came of it.

    {"at": "2026-09-21T17:40:03", "command": "check", "args": ["two-sum"], "exit": 0,
     "problem": "two-sum", "verdict": "Accepted", "passed": 15, "total": 15, "ms": 4}

It is yours, not the repo's: git ignores it. Writing it never gets in the way of the command itself.
"""

from __future__ import annotations

import json
from datetime import datetime

from .catalog import ROOT

PATH = ROOT / "journal.jsonl"


def record(argv: list[str], exit_code: int, **facts) -> None:
    entry = {"at": datetime.now().isoformat(timespec="seconds"), "command": argv[0] if argv else "",
             "args": argv[1:], "exit": exit_code, **{name: value for name, value in facts.items() if value is not None}}
    try:
        with PATH.open("a") as journal:
            journal.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except OSError:
        pass
