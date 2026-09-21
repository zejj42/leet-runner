"""leet: list problems, scaffold one, test one, find the next, open one in VS Code."""

from __future__ import annotations

import argparse
import json
import os
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
    new.add_argument("--force", action="store_true", help="refresh the test file; your solution, cases and README are kept")

    test = commands.add_parser("test", help="run a problem's tests (or every problem's)")
    test.add_argument("problem", nargs="?", help="leave out to test everything you have started")

    listing = commands.add_parser("list", help="what you have, and how it stands")
    listing.add_argument("--all", action="store_true", help="the whole list, including problems without a folder")

    commands.add_parser("setup", help="create the virtual environment and make ▶ on a solution.py run its tests")
    commands.add_parser("next", help="the first problem on the list you have not passed")
    opening = commands.add_parser("open", help="open a problem in VS Code")
    opening.add_argument("problem")

    args = parser.parse_args(argv)
    try:
        return {"new": _new, "test": _test, "list": _list, "next": _next, "open": _open, "setup": _setup}[args.command](args)
    except (LookupError, FileExistsError) as problem:
        print(f"leet: {problem}", file=sys.stderr)
        return 2


# ---- commands

def _setup(args) -> int:
    import sysconfig
    import venv
    environment = ROOT / ".venv"
    if not (environment / "bin" / "python").exists():
        print("Creating .venv ...")
        venv.create(environment, with_pip=True)
    python = environment / "bin" / "python"
    subprocess.check_call([str(python), "-m", "pip", "install", "-q", "-r", str(ROOT / "requirements.txt")])
    site = subprocess.check_output([str(python), "-c", "import sysconfig; print(sysconfig.get_paths()['purelib'])"], text=True).strip()
    # A .pth file: its first line puts this repo on the path, its second runs at every start of this Python.
    (Path(site) / "leetkit_autorun.pth").write_text(f"{ROOT}\nimport leetkit.autorun; leetkit.autorun.install()\n")
    link = Path.home() / ".local" / "bin" / "leet"          # `leet` from any folder, without the ./
    if link.is_symlink() or not link.exists():
        link.parent.mkdir(parents=True, exist_ok=True)
        link.unlink(missing_ok=True)
        link.symlink_to(ROOT / "leet")
    if str(link.parent) not in os.environ.get("PATH", "").split(os.pathsep):
        print(f"{link.parent} is not on your PATH, so keep typing ./leet from this folder.")
    from .colours import install
    if not install():
        print("VS Code's `code` command was not found, so the verdict in the Output panel stays uncoloured.")
    print("Ready. Open a solution.py and press ▶ (Run Python File) to test it.")
    return 0


def _new(args) -> int:
    from .scaffold import scaffold
    problem = find(args.problem)
    folder = scaffold(problem, force=args.force)
    print(f"{problem.label}  {problem.title}  ({problem.difficulty})")
    print(f"  {folder.relative_to(ROOT)}/solution.py   ← write here")
    print(f"  leet test {problem.label.lstrip('0') or '0'}")
    return 0


def _test(args) -> int:
    from .run import judge_and_report, judge_folder, one_line, remember
    if args.problem:
        problem = find(args.problem)
        if not problem.folder.exists():
            raise LookupError(f"{problem.title} has no folder yet. Create it with: leet new {args.problem}")
        return 0 if judge_and_report(problem.folder).verdict in ("Accepted", "Not started") else 1

    problems = [p for p in all_problems() if p.folder.exists()]
    if not problems:
        raise LookupError("Nothing to test yet. Start with: leet new 1")
    print()
    failed = 0
    for problem in problems:                                 # everything you have started: one line each
        result = judge_folder(problem.folder)
        remember(problem.folder, result)
        failed += result.verdict not in ("Accepted", "Not started")
        print(f"  {problem.label}  {problem.title:<46} {one_line(result)}")
    print()
    return 1 if failed else 0


def _list(args) -> int:
    results = _load_results()
    problems = all_problems() if args.all else [p for p in all_problems() if p.folder.exists()]
    if not problems:
        print("No problems yet. Start with: leet new 1      (the whole list: leet list --all)")
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
            print(f"  leet test {p.number or p.label}" if p.folder.exists() else f"  leet new {p.number or p.label}")
            return 0
    print("Every problem passes. Take a bow.")
    return 0


def _open(args) -> int:
    problem = find(args.problem)
    if not problem.folder.exists():
        raise LookupError(f"{problem.title} has no folder yet. Create it with: leet new {args.problem}")
    if shutil.which("code") is None:
        print(problem.folder)
        return 0
    return subprocess.call(["code", str(ROOT), str(problem.folder / "README.md"), str(problem.folder / "solution.py")])


# ---- remembering how each problem stands

def _load_results() -> dict:
    return json.loads(_RESULTS.read_text()) if _RESULTS.exists() else {}
