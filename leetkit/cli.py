"""leet: list the problems, read one, write it in Neovim or vim, check it, open it in VS Code, reset it to its empty state, set the repo up,
update it."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

from .catalog import ROOT, Problem, all_problems, find

_USAGE = """\
usage: leet <command> [<problem>] [options]

  list                     the problems in the repo, difficulty and category, 正 grows one stroke per solve
  read <problem>           print the problem's statement
  code <problem>           open its solution.py in nvim (vim if there is no nvim)
  check <problem>          judge solution.py: Accepted, Wrong Answer, Runtime Error, Time Limit Exceeded
  open <problem>           open the problem in VS Code
  reset <problem>          erase your code; the problem keeps its solves
      --progress           also forget its solves
      -y                   do not ask first
  startover                erase your code in every problem and forget all solves
      -y                   do not ask first
  setup                    create .venv, the leet command and the VS Code extension
  update                   pull the newest problems and kit from GitHub
  --version

<problem>  its number on the list (1), its LeetCode slug (two-sum), or words of its title (two sum)
"""


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
    parser = argparse.ArgumentParser(prog="leet", usage=_USAGE, add_help=False)
    parser.add_argument("-h", "--help", action="store_true")
    parser.add_argument("--version", action="version", version=f"leet-runner {version()}")
    commands = parser.add_subparsers(dest="command", metavar="<command>")
    def command(name: str, usage: str, problem: bool = False, yes: bool = False):
        sub = commands.add_parser(name, add_help=False, usage=f"leet {usage}")
        sub.add_argument("-h", "--help", action="store_true")   # -h anywhere prints the one help page
        if problem:
            sub.add_argument("problem", nargs="*")
        if yes:
            sub.add_argument("-y", "--yes", action="store_true")
        return sub
    for name in ("list", "setup", "update"):
        command(name, name)
    for name in ("read", "code", "check", "open"):
        command(name, f"{name} <problem>", problem=True)
    command("reset", "reset <problem> [--progress] [-y]", problem=True, yes=True).add_argument("--progress", action="store_true")
    command("startover", "startover [-y]", yes=True)

    args = parser.parse_args(argv)
    if args.help or args.command is None:
        print(_USAGE.rstrip("\n"))
        return 0
    if getattr(args, "problem", None) == []:
        parser.exit(2, f"leet {args.command}: which problem? {_USAGE.splitlines()[-1].lstrip('<problem> ')}\n")
    args.facts = facts                                      # what a command adds to its line in the journal
    try:
        return {"list": _list, "read": _read, "code": _code, "check": _check, "open": _open, "reset": _reset, "startover": _startover, "setup": _setup, "update": _update}[args.command](args)
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
    print("Ready:  leet code two-sum   then   leet check two-sum")
    return 0


def _check(args) -> int:
    from .run import judge_and_report
    problem = _in_the_repo(args.problem)
    args.facts["problem"] = problem.slug
    result = judge_and_report(problem.folder)
    args.facts.update(verdict=result.verdict, passed=result.passed, total=result.total, failed_case=result.case or None,
                      ms=result.milliseconds if result.accepted else None)
    return 0 if result.verdict in ("Accepted", "Not started") else 1


def _list(args) -> int:
    colours = {"easy": "32", "medium": "33", "hard": "31"}
    terminal = sys.stdout.isatty()
    problems = [problem for problem in all_problems() if problem.folder.exists()]
    width = max((len(problem.title) for problem in problems), default=0)
    topics = {problem.slug: _topic(problem) for problem in problems}
    topic_width = max((len(topic) for topic in topics.values()), default=0)
    from .progress import solves
    done = solves()
    lines = []
    for problem in problems:
        level = f"{problem.difficulty:<6}"
        mark = _strokes(done.get(problem.slug, 0), terminal)
        extra = f"{'extra' if problem.number is None else '':<5}"       # not one of the 169 on the chart
        topic = f"{topics[problem.slug]:<{topic_width}}"
        if terminal:
            level = f"\033[{colours.get(problem.difficulty, '0')}m{level}\033[0m"
            extra = f"\033[1;35m{extra}\033[0m"
            topic = f"\033[36m{topic}\033[0m"
        lines.append(f"{mark}  {problem.label:<6}  {problem.title:<{width}}  {level}  {topic}  {extra}".rstrip())
    count = sum(problem.slug in done for problem in problems)
    lines.append(f"\n{count} of {len(problems)} solved.  leet read <number or title>")
    _show("\n".join(lines))
    return 0


# 正 as it is written, a stroke at a time: one solve shows 一, two 丅, then 下, 止 and the whole 正, which stays from five
# solves on. (止 is the nearest real character to the four-stroke stage.) The Linux text console has no Chinese
# characters at all, so there, and wherever LEET_TALLY=plain says so, the number of solves is shown instead.
_ZHENG = {"cjk": ["　", "一", "丅", "下", "止", "正"], "plain": ["  ", "1 ", "2 ", "3 ", "4 ", "5 "]}


def _stroke_style() -> str:
    asked = os.environ.get("LEET_TALLY", "").lower()
    if asked in _ZHENG:
        return asked
    utf8 = "utf" in (getattr(sys.stdout, "encoding", "") or "").lower()
    return "plain" if os.environ.get("TERM") == "linux" or not utf8 else "cjk"


def _strokes(solved: int, terminal: bool) -> str:
    stages = _ZHENG[_stroke_style()]
    mark = stages[min(solved, len(stages) - 1)]
    return f"\033[1;32m{mark}\033[0m" if terminal and solved else mark


def _topic(problem: Problem) -> str:
    """The list writes its topics two ways, linkedList and Two Pointers. Here they all read alike: linked list."""
    import re
    return re.sub(r"(?<=[a-z])(?=[A-Z])", " ", problem.topic).lower()


def _show(text: str) -> None:
    """As git does: a list taller than the terminal goes through less (space for the next page, q to leave); one that
    fits is simply printed, and so is anything that is piped somewhere."""
    rows = shutil.get_terminal_size((80, 24)).lines
    if sys.stdout.isatty() and text.count("\n") + 2 > rows and shutil.which("less"):
        subprocess.run(["less", "-FRX"], input=text + "\n", text=True)
    else:
        print(text)


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
    from . import progress
    solution = problem.folder / "solution.py"
    empty = not solution.exists() or solution.read_text() == problem.stub.read_text()
    solves = progress.solves().get(problem.slug, 0)
    if empty and not (args.progress and solves):
        print(f"{problem.title} is already in its starting state.")
        return 0
    if not args.yes:
        doing = [] if empty else [f"erases your code in {solution.relative_to(ROOT)}"]
        if args.progress and solves:
            doing.append(f"forgets its {solves} solve{'' if solves == 1 else 's'}")
        if input(f"This {' and '.join(doing)}. Go on? [y/N] ").strip().lower() not in ("y", "yes"):
            print("Left as it is.")
            return 1
    solution.write_text(problem.stub.read_text())
    if args.progress:
        progress.forget(problem.slug)
    else:
        progress.note_reset(problem.slug)                   # its strokes stay; the next Accepted adds one
    args.facts.update(erased=not empty, forgotten=solves if args.progress else 0)
    print(f"{problem.title} is back to its starting state" + (", unsolved." if args.progress else "."))
    return 0


def _startover(args) -> int:
    from . import progress
    written = [problem for problem in all_problems()
               if problem.stub.exists() and (problem.folder / "solution.py").exists()
               and (problem.folder / "solution.py").read_text() != problem.stub.read_text()]
    marks = len(progress.solves())
    args.facts.update(erased=0, forgotten=0)
    if not written and not marks:
        print("Nothing to start over from: no code written, nothing marked solved.")
        return 0
    if not args.yes:
        print(f"This erases your code in {len(written)} problem{'' if len(written) == 1 else 's'}"
              f" and forgets the strokes of {marks} problem{'' if marks == 1 else 's'}. The cases and the journal stay.")
        for problem in written:
            print(f"  · {problem.title}")
        if input("Start over? [y/N] ").strip().lower() not in ("y", "yes"):
            print("Left as it is.")
            return 1
    for problem in written:
        (problem.folder / "solution.py").write_text(problem.stub.read_text())
    progress.forget_all()
    args.facts.update(erased=len(written), forgotten=marks)
    print("Started over: every problem is empty and unsolved again.")
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
    problem = find(" ".join(words))                          # leet check two sum, without quotes, works too
    if not problem.folder.exists():
        raise LookupError(f"{problem.title} is on the list, but its folder is not in the repo yet.")
    if not (problem.folder / "solution.py").exists() and problem.stub.exists():
        (problem.folder / "solution.py").write_text(problem.stub.read_text())
    return problem
