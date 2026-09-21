"""./leet: list problems, scaffold one, test one, find the next, open one in VS Code."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

from .catalog import ROOT, Problem, all_problems, find

_RESULTS = ROOT / ".leet" / "results.json"
_MARK = {"passed": "✓", "failed": "✗", "not started": "·", None: " "}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="leet", description="Practice the LeetTracker list locally.")
    commands = parser.add_subparsers(dest="command", required=True)

    new = commands.add_parser("new", help="create a problem's folder from LeetCode")
    new.add_argument("problem", help="chart number, lc<id>, slug, or part of the title")
    new.add_argument("--force", action="store_true", help="refresh README, cases and test file; solution.py is kept")

    test = commands.add_parser("test", help="run a problem's tests (or every problem's)")
    test.add_argument("problem", nargs="?", help="leave out to test everything you have started")
    test.add_argument("--stress", action="store_true", help="also run the large, slow cases")
    test.add_argument("-v", "--verbose", action="store_true")

    listing = commands.add_parser("list", help="what you have, and how it stands")
    listing.add_argument("--all", action="store_true", help="the whole list, including problems without a folder")

    commands.add_parser("next", help="the first problem on the list you have not passed")
    opening = commands.add_parser("open", help="open a problem in VS Code")
    opening.add_argument("problem")

    args = parser.parse_args(argv)
    try:
        return {"new": _new, "test": _test, "list": _list, "next": _next, "open": _open}[args.command](args)
    except (LookupError, FileExistsError) as problem:
        print(f"leet: {problem}", file=sys.stderr)
        return 2


# ---- commands

def _new(args) -> int:
    from .scaffold import scaffold
    problem = find(args.problem)
    folder = scaffold(problem, force=args.force)
    print(f"{problem.label}  {problem.title}  ({problem.difficulty})")
    print(f"  {folder.relative_to(ROOT)}/solution.py   ← write here")
    print(f"  ./leet test {problem.label.lstrip('0') or '0'}")
    return 0


def _test(args) -> int:
    if args.problem:
        problem = find(args.problem)
        if not problem.folder.exists():
            raise LookupError(f"{problem.title} has no folder yet. Create it with: ./leet new {args.problem}")
        targets, problems = [str(problem.folder)], [problem]
    else:
        problems = [p for p in all_problems() if p.folder.exists()]
        targets = [str(p.folder) for p in problems]
        if not targets:
            raise LookupError("Nothing to test yet. Start with: ./leet new 1")

    report = ROOT / ".leet" / "last-run.xml"
    report.parent.mkdir(exist_ok=True)
    command = [sys.executable, "-m", "pytest", *targets, f"--junitxml={report}", "-q", "--no-header", "-rN",
               "--tb=short", "-p", "no:cacheprovider"]
    command += ["--stress"] if args.stress else []
    command += ["-v"] if args.verbose else []
    code = subprocess.call(command, cwd=ROOT)
    print()
    for problem, counts in _record(report, problems):
        print(f"  {_verdict(counts)}  {problem.label}  {problem.title}")
    return code


def _verdict(counts: dict) -> str:
    ran = counts["passed"] + counts["failed"]
    held_back = f"   ({counts['skipped']} stress held back: --stress)" if counts["skipped"] else ""
    if counts["timed out before"]:
        return f"✗ ran out of time; {counts['timed out before']} later cases were not run"
    if counts["failed"]:
        return f"✗ {counts['failed']} of {ran} {'case' if ran == 1 else 'cases'} failed{held_back}"
    if ran == 0:
        return "· not started"
    return f"✓ {'the one case' if ran == 1 else f'all {ran} cases'} passed{held_back}"


def _list(args) -> int:
    results = _load_results()
    problems = all_problems() if args.all else [p for p in all_problems() if p.folder.exists()]
    if not problems:
        print("No problems yet. Start with: ./leet new 1      (the whole list: ./leet list --all)")
        return 0
    section = None
    for p in problems:
        heading = f"{p.list}  {p.section}".strip()
        if heading != section:
            section = heading
            print(f"\n{heading}")
        state = results.get(p.label) if p.folder.exists() else None
        folder = "" if p.folder.exists() else "   (no folder)"
        print(f"  {_MARK.get(state, '?')} {p.label}  {p.title:<52} {p.difficulty:<7}{folder}")
    print("\n  ✓ passed   ✗ failing   · not started")
    return 0


def _next(args) -> int:
    results = _load_results()
    for p in all_problems():
        if results.get(p.label) != "passed":
            print(f"{p.label}  {p.title}  ({p.difficulty}, {p.topic})")
            print(f"  ./leet test {p.number or p.label}" if p.folder.exists() else f"  ./leet new {p.number or p.label}")
            return 0
    print("Every problem passes. Take a bow.")
    return 0


def _open(args) -> int:
    problem = find(args.problem)
    if not problem.folder.exists():
        raise LookupError(f"{problem.title} has no folder yet. Create it with: ./leet new {args.problem}")
    if shutil.which("code") is None:
        print(problem.folder)
        return 0
    return subprocess.call(["code", str(ROOT), str(problem.folder / "README.md"), str(problem.folder / "solution.py")])


# ---- remembering how each problem stands

def _load_results() -> dict:
    return json.loads(_RESULTS.read_text()) if _RESULTS.exists() else {}


def _record(report: Path, problems: list[Problem]) -> list[tuple[Problem, dict]]:
    """Reads pytest's report, remembers how each problem stands, and hands back the counts for the summary."""
    import xml.etree.ElementTree as ET
    if not report.exists():
        return []
    by_folder: dict[str, list[str]] = {}
    for case in ET.parse(report).getroot().iter("testcase"):
        folder = next((part for part in case.get("classname", "").split(".") if part[:3].isdigit() or part.startswith("lc")), None)
        if folder is None:
            continue
        failed = case.find("failure") is not None or case.find("error") is not None
        skipped = case.find("skipped")
        not_started = skipped is not None and "not started" in (skipped.get("message") or "")
        message = (skipped.get("message") or "") if skipped is not None else ""
        state = ("failed" if failed else "not started" if not_started else "timed out before" if "ran out of time" in message
                 else "skipped" if skipped is not None else "passed")
        by_folder.setdefault(folder, []).append(state)

    results, summary = _load_results(), []
    for p in problems:
        states = by_folder.get(p.folder.name, [])
        if not states:
            continue
        counts = {state: states.count(state) for state in ("passed", "failed", "not started", "skipped", "timed out before")}
        # Stress cases that were held back do not count against you.
        results[p.label] = "failed" if counts["failed"] else "passed" if counts["passed"] else "not started"
        summary.append((p, counts))
    _RESULTS.parent.mkdir(exist_ok=True)
    _RESULTS.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")
    return summary
