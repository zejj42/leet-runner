"""leet: write a problem in vim, test it, open it in VS Code, reset it to its empty state, set the repo up."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

from .catalog import ROOT, Problem, find

_PROBLEM = "its number on the list (1), its LeetCode slug (two-sum), or words from its title"


def main(argv: list[str] | None = None) -> int:
    """Runs the command, and writes it in the journal however it ended: done, refused, or not even understood."""
    from . import journal
    argv = list(sys.argv[1:] if argv is None else argv)
    facts: dict = {}
    code = 1
    try:
        code = _run(argv, facts)
        return code
    except SystemExit as leaving:                           # argparse: --help, or a command it does not know
        code = leaving.code if isinstance(leaving.code, int) else 1
        raise
    except KeyboardInterrupt:
        code = 130
        raise
    finally:
        journal.record(argv, code, **facts)


def _run(argv: list[str], facts: dict) -> int:
    parser = argparse.ArgumentParser(prog="leet", description="Practice the LeetTracker list locally.")
    commands = parser.add_subparsers(dest="command", required=True, metavar="{code,test,open,reset,setup}")
    commands.add_parser("code", help="edit a problem's solution.py in vim").add_argument("problem", nargs="+", help=_PROBLEM)
    commands.add_parser("test", help="judge your solution to a problem").add_argument("problem", nargs="+", help=_PROBLEM)
    commands.add_parser("open", help="open a problem in VS Code").add_argument("problem", nargs="+", help=_PROBLEM)
    reset = commands.add_parser("reset", help="put a problem's solution.py back to its empty starting state")
    reset.add_argument("problem", nargs="+", help=_PROBLEM)
    reset.add_argument("-y", "--yes", action="store_true", help="do not ask first")
    commands.add_parser("setup", help="create the virtual environment, the `leet` command and ▶ on a solution.py")

    args = parser.parse_args(argv)
    args.facts = facts                                      # what a command adds to its line in the journal
    try:
        return {"code": _code, "test": _test, "open": _open, "reset": _reset, "setup": _setup}[args.command](args)
    except LookupError as problem:
        print(f"leet: {problem}", file=sys.stderr)
        facts["error"] = str(problem)
        return 2


# ---- commands

def _setup(args) -> int:
    import sysconfig
    import venv
    # Judging needs nothing but Python itself, so the environment is made without pip. That matters on Debian and
    # Ubuntu, where pip-in-a-venv is a separate package (python3-venv) that a fresh machine does not have.
    environment = ROOT / ".venv"
    python = environment / "bin" / "python"
    if not python.exists():
        print("Creating .venv ...")
        venv.create(environment, with_pip=False)
    site = subprocess.check_output([str(python), "-c", "import sysconfig; print(sysconfig.get_paths()['purelib'])"], text=True).strip()
    # A .pth file: its first line puts this repo on the path, its second runs at every start of this Python.
    (Path(site) / "leetkit_autorun.pth").write_text(f"{ROOT}\nimport leetkit.autorun; leetkit.autorun.install()\n")
    link = Path.home() / ".local" / "bin" / "leet"          # `leet` from any folder, without the ./
    if link.is_symlink() or not link.exists():
        link.parent.mkdir(parents=True, exist_ok=True)
        link.unlink(missing_ok=True)
        link.symlink_to(ROOT / "leet")
    if str(link.parent) not in os.environ.get("PATH", "").split(os.pathsep):
        print(f"{link.parent} is not on your PATH yet. Until it is, run ./leet from this folder.")
    from .colours import install
    install()                                               # only if VS Code is here; without it there is nothing to colour
    print("Ready:  leet code two-sum   then   leet test two-sum")
    return 0


def _test(args) -> int:
    from .run import judge_and_report
    problem = _in_the_repo(args.problem)
    args.facts["problem"] = problem.slug
    result = judge_and_report(problem.folder)
    args.facts.update(verdict=result.verdict, passed=result.passed, total=result.total, failed_case=result.case or None,
                      ms=result.milliseconds if result.accepted else None)
    return 0 if result.verdict in ("Accepted", "Not started") else 1


def _code(args) -> int:
    problem = _in_the_repo(args.problem)
    args.facts["problem"] = problem.slug
    if shutil.which("vim") is None:
        raise LookupError("vim was not found on this machine.")
    # vim starts inside the problem's folder, so :e cases.json and :e README.md are right there
    return subprocess.call(["vim", "solution.py"], cwd=problem.folder)


def _open(args) -> int:
    problem = _in_the_repo(args.problem)
    args.facts["problem"] = problem.slug
    if shutil.which("code") is None:
        print(problem.folder)
        return 0
    return subprocess.call(["code", str(ROOT), str(problem.folder / "README.md"), str(problem.folder / "solution.py")])


def _reset(args) -> int:
    problem = _in_the_repo(args.problem)
    args.facts.update(problem=problem.slug, erased=False)
    if not problem.stub.exists():
        raise LookupError(f"{problem.title} has no starting file saved in {problem.stub.parent.relative_to(ROOT)}.")
    solution = problem.folder / "solution.py"
    if solution.exists() and solution.read_text() == problem.stub.read_text():
        print(f"{problem.title} is already in its starting state.")
        return 0
    if not args.yes:
        answer = input(f"This erases your code in {solution.relative_to(ROOT)}. Go on? [y/N] ")
        if answer.strip().lower() not in ("y", "yes"):
            print("Left as it is.")
            return 1
    solution.write_text(problem.stub.read_text())
    args.facts["erased"] = True
    print(f"{problem.title} is back to its starting state.")
    return 0


def _in_the_repo(words: list[str]) -> Problem:
    problem = find(" ".join(words))                          # leet test two sum, without quotes, works too
    if not problem.folder.exists():
        raise LookupError(f"{problem.title} is on the list, but its folder is not in the repo yet.")
    return problem
