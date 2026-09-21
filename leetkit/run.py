"""Judges one problem and reports it the way LeetCode does: one verdict with the count of cases passed, and,
when it is not Accepted, the first case that went wrong and nothing after it.

This is what pressing ▶ on a solution.py shows, and what `leet test` prints.
"""

from __future__ import annotations

import contextlib
import io
import sys
import time
from dataclasses import dataclass
from pathlib import Path

from .judge import NotStarted, WrongAnswer, describe, load_spec, run_case


@dataclass
class Result:
    verdict: str              # Accepted, Wrong Answer, Time Limit Exceeded, Runtime Error, Not started
    passed: int = 0
    total: int = 0
    case: str = ""            # the first case that went wrong
    details: str = ""
    milliseconds: int = 0
    stdout: str = ""          # what your code printed during the case shown: the failing one, or else the first
    stdout_case: str = ""

    @property
    def accepted(self) -> bool:
        return self.verdict == "Accepted"


def judge_folder(folder: Path) -> Result:
    """Runs the cases in order and stops at the first that does not pass, as LeetCode does."""
    spec = load_spec(folder)
    cases = spec.cases
    result = Result("Accepted", total=len(cases))
    started = time.perf_counter()
    for index, case in enumerate(cases):
        printed = io.StringIO()
        try:
            with contextlib.redirect_stdout(printed):       # prints are shown with the case they belong to, as on LeetCode
                run_case(spec, case)
        except NotStarted:
            return Result("Not started", total=len(cases))
        except WrongAnswer as wrong:
            result.verdict, result.case, result.details = wrong.verdict, case.name, str(wrong)
            result.stdout, result.stdout_case = printed.getvalue(), case.name
            break
        except Exception as crash:                         # your code raised: say what, and where in your file
            where = _line_in(crash, folder)
            error = f"  {type(crash).__name__}: {crash}" + (f"     line {where}" if where else "")
            result.verdict, result.case = "Runtime Error", case.name
            result.details = error + "\n" + describe(spec, case, input_label="Last input")
            result.stdout, result.stdout_case = printed.getvalue(), case.name
            break
        if index == 0:
            result.stdout, result.stdout_case = printed.getvalue(), case.name
        result.passed += 1
    result.milliseconds = round((time.perf_counter() - started) * 1000)
    return result


def _line_in(crash: Exception, folder: Path):
    trace, line = crash.__traceback__, None
    while trace is not None:
        if Path(trace.tb_frame.f_code.co_filename).parent == folder:
            line = trace.tb_lineno
        trace = trace.tb_next
    return line


# ---- printing

def _paint(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m" if sys.stdout.isatty() else text


def one_line(result: Result) -> str:
    """"Accepted   14 / 14 testcases passed   3 ms", in green or red."""
    if result.verdict == "Not started":
        return _paint("Not started", "2") + "   the method still raises NotImplementedError"
    colour = "1;32" if result.accepted else "1;31"
    line = f"{_paint(result.verdict, colour)}   {result.passed} / {result.total} testcases passed"
    return line + (_paint(f"   {result.milliseconds} ms", "2") if result.accepted else "")


def report(title: str, result: Result) -> str:
    lines = [f"{_paint(title, '1')}   {one_line(result)}"]
    printed = _stdout_block(result.stdout)
    if result.details:
        details = result.details.split("\n")
        # the prints go where LeetCode puts them: after the input, before your output
        at = next((i for i, line in enumerate(details) if line.startswith(("  Output", "  Expected"))), len(details))
        lines += ["", _paint(f"  {result.case}", "2")] + details[:at] + printed + details[at:]
    elif printed:                                           # nothing went wrong: the first case's prints, as a sample
        lines += ["", _paint(f"  {result.stdout_case}", "2")] + printed
    return "\n".join(lines)


def _stdout_block(text: str, most: int = 30) -> list[str]:
    rows = text.rstrip("\n").split("\n") if text.strip() else []
    if len(rows) > most:
        rows = rows[:most] + [f"... and {len(rows) - most} more lines"]
    rows = [row if len(row) <= 300 else row[:300] + " ..." for row in rows]
    return [f"  {'Stdout' if index == 0 else '':<12}{_paint(row, '36')}" for index, row in enumerate(rows)]


def title_of(folder: Path) -> str:
    from .catalog import find
    try:
        return find(folder.name).title
    except LookupError:
        return folder.name


def judge_and_report(folder: Path) -> Result:
    result = judge_folder(folder)
    print(report(title_of(folder), result))
    if result.accepted:
        _note_solved(folder)
    return result


def _note_solved(folder: Path) -> None:
    """For `leet list`. Only a problem of this repo counts, not a copy of its folder somewhere else."""
    from . import catalog
    from .progress import mark_solved
    if folder.resolve().parent != catalog.PROBLEMS_DIR.resolve():
        return
    try:
        mark_solved(catalog.find(folder.name).slug)
    except LookupError:
        pass

