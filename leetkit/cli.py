"""leet: read a problem, write it in Neovim or vim, test it, open it in VS Code, reset it to its empty state, set the repo up,
update it."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

from .catalog import ROOT, Problem, all_problems, find

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
    from .version import version
    parser = argparse.ArgumentParser(prog="leet", description="Practice the LeetTracker list locally.")
    parser.add_argument("--version", action="version", version=f"leet-runner {version()}")
    commands = parser.add_subparsers(dest="command", required=True, metavar="{read,code,test,open,reset,setup,update}")
    commands.add_parser("read", help="show a problem's statement").add_argument("problem", nargs="+", help=_PROBLEM)
    commands.add_parser("code", help="edit a problem's solution.py in Neovim (or vim, if there is no nvim)").add_argument("problem", nargs="+", help=_PROBLEM)
    commands.add_parser("test", help="judge your solution to a problem").add_argument("problem", nargs="+", help=_PROBLEM)
    commands.add_parser("open", help="open a problem in VS Code").add_argument("problem", nargs="+", help=_PROBLEM)
    reset = commands.add_parser("reset", help="put a problem's solution.py back to its empty starting state")
    reset.add_argument("problem", nargs="+", help=_PROBLEM)
    reset.add_argument("-y", "--yes", action="store_true", help="do not ask first")
    commands.add_parser("setup", help="create the virtual environment, the `leet` command and ▶ on a solution.py")

    commands.add_parser("update", help="get the newest problems and kit from GitHub; your solutions are left alone")

    args = parser.parse_args(argv)
    args.facts = facts                                      # what a command adds to its line in the journal
    try:
        return {"read": _read, "code": _code, "test": _test, "open": _open, "reset": _reset, "setup": _setup, "update": _update}[args.command](args)
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
        print(f"The leet command is now in {link.parent}, a folder your shell does not search for commands yet (it is\n"
              "not on your PATH). On Ubuntu, logging out and back in adds it. Until then, type ./leet from this folder.\n")
    lay_out_solutions()
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


def _read(args) -> int:
    from .reader import render
    problem = _in_the_repo(args.problem)
    args.facts["problem"] = problem.slug
    print(render((problem.folder / "README.md").read_text(), colour=sys.stdout.isatty()))
    return 0


def _code(args) -> int:
    problem = _in_the_repo(args.problem)
    args.facts["problem"] = problem.slug
    editor = next((name for name in ("nvim", "vim") if shutil.which(name)), None)      # Neovim first
    if editor is None:
        raise LookupError("Neither nvim nor vim was found on this machine.")
    args.facts["editor"] = editor
    # The editor starts inside the problem's folder, so :e cases.json and :e README.md are right there.
    return subprocess.call([editor, "solution.py"], cwd=problem.folder)


def _open(args) -> int:
    problem = _in_the_repo(args.problem)
    args.facts["problem"] = problem.slug
    # VS Code needs a screen to open a window on. Over ssh there is none, unless this is VS Code's own remote terminal.
    over_ssh = "SSH_CONNECTION" in os.environ and os.environ.get("TERM_PROGRAM") != "vscode"
    if shutil.which("code") is None or over_ssh:
        why = "this is an ssh session, with no screen for VS Code to open on" if over_ssh else "VS Code's `code` command is not on this machine"
        print(f"Not opened: {why}.\nEdit it here instead:  leet code {problem.slug}\nIts folder:  {problem.folder}")
        return 1
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


def _update(args) -> int:
    """There is nothing to build: the kit runs from its source. Updating is a git pull, then setup once more, run
    by the new code, for whatever that setup has learnt to do. Solutions are not in git, so a pull cannot touch them;
    a cases.json you added cases to is set aside and put back by --autostash."""
    if not (ROOT / ".git").exists():
        raise LookupError("This copy was not made with git clone, so it cannot update itself.")
    from .version import version
    had, was, version_was = _folders(), _commit(), version(ROOT)
    pull = subprocess.run(["git", "-C", str(ROOT), "pull", "--ff-only", "--autostash"], capture_output=True, text=True)
    if pull.returncode != 0:
        print(f"Not updated. git says:\n\n{(pull.stderr or pull.stdout).strip()}")
        return 1
    if _commit() == was:
        print(f"Already up to date, at {version_was}.")
        return 0
    new = sorted(_folders() - had)
    changes = subprocess.check_output(["git", "-C", str(ROOT), "log", "--reverse", "--format=%s", f"{was}..HEAD"], text=True).splitlines()
    args.facts.update(was=version_was, now=version(ROOT), new_problems=new, changes=changes)
    print(f"Updated  {version_was} → {version(ROOT)}\n\nWhat changed:")
    for change in changes:
        print(f"  · {change}")
    if new:                                                 # "problems" alone would read as trouble
        print("\nLeetCode problems added to the set:")
        for name in new:
            print(f"  · {find(name).title}     leet read {find(name).slug}")
    return _setup_again()


def _setup_again() -> int:
    return subprocess.call([str(ROOT / "leet"), "setup"], stdout=subprocess.DEVNULL)     # a new process: the new code


def _commit() -> str:
    return subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "--short", "HEAD"], text=True).strip()


def _folders() -> set[str]:
    return {problem.folder.name for problem in all_problems() if problem.folder.exists()}


def lay_out_solutions() -> None:
    """A solution.py is yours, so git does not track it. Where a problem has none yet, it gets its empty stub."""
    for problem in all_problems():
        solution = problem.folder / "solution.py"
        if problem.folder.exists() and problem.stub.exists() and not solution.exists():
            solution.write_text(problem.stub.read_text())


def _in_the_repo(words: list[str]) -> Problem:
    problem = find(" ".join(words))                          # leet test two sum, without quotes, works too
    if not problem.folder.exists():
        raise LookupError(f"{problem.title} is on the list, but its folder is not in the repo yet.")
    if not (problem.folder / "solution.py").exists() and problem.stub.exists():
        (problem.folder / "solution.py").write_text(problem.stub.read_text())
    return problem
