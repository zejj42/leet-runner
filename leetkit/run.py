"""Judges one problem and reports it the way LeetCode does: one verdict with the count of cases passed, and,
when it is not Accepted, the first case that went wrong and nothing after it.

    python -m leetkit.run problems/001_two_sum

This is what pressing ▶ on a solution.py shows, and what `leet test` prints.
"""

from __future__ import annotations

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

    @property
    def accepted(self) -> bool:
        return self.verdict == "Accepted"


def judge_folder(folder: Path, stress: bool = True) -> Result:
    """Runs the cases in order and stops at the first that does not pass, as LeetCode does."""
    spec = load_spec(folder)
    cases = [case for case in spec.cases if stress or not case.stress]
    result = Result("Accepted", total=len(cases))
    started = time.perf_counter()
    for case in cases:
        try:
            run_case(spec, case, stress=stress)
        except NotStarted:
            return Result("Not started", total=len(cases))
        except WrongAnswer as wrong:
            result.verdict, result.case, result.details = wrong.verdict, case.name, str(wrong)
            break
        except Exception as crash:                         # your code raised: say what, and where in your file
            where = _line_in(crash, folder)
            error = f"  {type(crash).__name__}: {crash}" + (f"     line {where}" if where else "")
            result.verdict, result.case = "Runtime Error", case.name
            result.details = error + "\n" + describe(spec, case, input_label="Last input")
            break
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
    if result.details:
        lines += ["", _paint(f"  {result.case}", "2"), result.details]
    return "\n".join(lines)


def title_of(folder: Path) -> str:
    from .catalog import find
    try:
        return find(folder.name).title
    except LookupError:
        return folder.name


def judge_and_report(folder: Path) -> Result:
    result = judge_folder(folder)
    print(report(title_of(folder), result))
    return result


def main(argv: list[str]) -> int:
    folder = Path(argv[0]).resolve()
    folder = folder.parent if folder.is_file() else folder
    return 0 if judge_and_report(folder).verdict in ("Accepted", "Not started") else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
