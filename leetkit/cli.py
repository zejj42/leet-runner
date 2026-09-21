"""leet: test a problem, open one in VS Code, set the repo up."""

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
    parser = argparse.ArgumentParser(prog="leet", description="Practice the LeetTracker list locally.")
    commands = parser.add_subparsers(dest="command", required=True, metavar="{test,open,setup}")
    commands.add_parser("test", help="judge your solution to a problem").add_argument("problem", nargs="+", help=_PROBLEM)
    commands.add_parser("open", help="open a problem in VS Code").add_argument("problem", nargs="+", help=_PROBLEM)
    commands.add_parser("setup", help="create the virtual environment, the `leet` command and ▶ on a solution.py")

    args = parser.parse_args(argv)
    try:
        return {"test": _test, "open": _open, "setup": _setup}[args.command](args)
    except LookupError as problem:
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


def _test(args) -> int:
    from .run import judge_and_report
    return 0 if judge_and_report(_in_the_repo(args.problem).folder).verdict in ("Accepted", "Not started") else 1


def _open(args) -> int:
    problem = _in_the_repo(args.problem)
    if shutil.which("code") is None:
        print(problem.folder)
        return 0
    return subprocess.call(["code", str(ROOT), str(problem.folder / "README.md"), str(problem.folder / "solution.py")])


def _in_the_repo(words: list[str]) -> Problem:
    problem = find(" ".join(words))                          # leet test two sum, without quotes, works too
    if not problem.folder.exists():
        raise LookupError(f"{problem.title} is on the list, but its folder is not in the repo yet.")
    return problem
