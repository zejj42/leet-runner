"""What makes ▶ work: running a problem's solution.py as a script judges it.

A solution.py holds only your class, so running it would do nothing. `./leet setup` puts one line in the
virtual environment (a .pth file) that calls install() whenever Python starts. install() looks at what is
being run, and only if it is a solution.py sitting next to a cases.json does it arrange for the judge to
run once the file has finished loading. Everything else Python does in this environment is left alone.
"""

from __future__ import annotations

import atexit
import sys
from pathlib import Path


_installed = False


def install() -> None:
    global _installed
    if _installed:                             # Python may read the .pth more than once as it starts
        return
    _installed = True
    try:
        script = Path(sys.argv[0]) if sys.argv and sys.argv[0] else None
        # Code Runner runs a selection from a temporary copy with this name; it still means "judge this problem".
        if script is None or script.name not in ("solution.py", "tempCodeRunnerFile.py"):
            return
        folder = script.resolve().parent
        if (folder / "cases.json").exists():
            atexit.register(_judge, folder)
    except Exception:
        pass                                   # never get in the way of Python starting


def _judge(folder: Path) -> None:
    if getattr(sys, "last_value", None) is not None or getattr(sys, "last_exc", None) is not None:
        return                                 # the file itself failed to load; Python has already said why
    from .run import judge_and_report
    judge_and_report(folder)
