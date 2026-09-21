"""Judges one problem and prints the verdicts, case by case. This is what pressing ▶ on a solution.py shows.

    python -m leetkit.run problems/001_two_sum [--stress]
"""

from __future__ import annotations

import sys
from pathlib import Path

from .judge import NotStarted, WrongAnswer, load_spec, run_case


def _paint(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m" if sys.stdout.isatty() else text


def green(text: str) -> str: return _paint(text, "32")
def red(text: str) -> str: return _paint(text, "31")
def dim(text: str) -> str: return _paint(text, "2")
def bold(text: str) -> str: return _paint(text, "1")


def judge_folder(folder: Path, stress: bool = False) -> dict:
    """Prints as it goes and returns the counts: passed, failed, held back (stress), and whether it was started."""
    spec = load_spec(folder)
    counts = {"passed": 0, "failed": 0, "held_back": 0, "started": True, "timed_out": False}
    title = folder.name.split("_", 1)[-1].replace("_", " ").title()
    print(bold(f"\n{title}") + dim(f"   {len(spec.cases)} cases"))

    for index, case in enumerate(spec.cases):
        if case.stress and not stress:
            counts["held_back"] += 1
            continue
        try:
            run_case(spec, case, stress=stress)
        except NotStarted:
            counts["started"] = False
            print(dim("  · not started: the method still raises NotImplementedError"))
            return counts
        except WrongAnswer as wrong:
            counts["failed"] += 1
            print(red(f"  ✗ {case.name}"))
            print("\n".join(f"      {line}" for line in str(wrong).split("\n") if line.strip()))
            if str(wrong).startswith("Time limit"):
                counts["timed_out"] = True
                left = sum(1 for later in spec.cases[index + 1:] if stress or not later.stress)
                if left:
                    print(dim(f"  · {left} later cases not run: they would only run out of time too"))
                break
        except Exception as crash:                         # your code raised: say where, in your file
            counts["failed"] += 1
            print(red(f"  ✗ {case.name}"))
            print(f"      {_where(crash, folder)}{type(crash).__name__}: {crash}")
        else:
            counts["passed"] += 1
            print(green(f"  ✓ {case.name}"))

    ran = counts["passed"] + counts["failed"]
    line = green(f"all {ran} passed") if not counts["failed"] else red(f"{counts['failed']} of {ran} failed")
    if counts["held_back"]:
        line += dim(f"   ·   {counts['held_back']} stress case held back (./leet test --stress)")
    print(f"\n  {line}\n")
    return counts


def _where(crash: Exception, folder: Path) -> str:
    trace = crash.__traceback__
    spot = None
    while trace is not None:
        if Path(trace.tb_frame.f_code.co_filename).parent == folder:
            spot = trace
        trace = trace.tb_next
    return f"line {spot.tb_lineno}: " if spot else ""


def remember(folder: Path, counts: dict) -> None:
    """So that ./leet list and ./leet next know how this problem stands."""
    import json
    from .catalog import PROBLEMS_DIR, ROOT, find
    if folder.resolve().parent != PROBLEMS_DIR.resolve():
        return                                  # a copy somewhere else is not this repo's progress
    try:
        label = find(folder.name).label
    except LookupError:
        return
    path = ROOT / ".leet" / "results.json"
    results = json.loads(path.read_text()) if path.exists() else {}
    results[label] = "not started" if not counts["started"] else "failed" if counts["failed"] else "passed"
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")


def main(argv: list[str]) -> int:
    folder = Path(argv[0]).resolve()
    folder = folder.parent if folder.is_file() else folder
    counts = judge_folder(folder, stress="--stress" in argv)
    remember(folder, counts)
    return 1 if counts["failed"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
