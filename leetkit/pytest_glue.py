"""What a problem's test_solution.py calls to get its tests: one pytest case per entry in cases.json."""

from __future__ import annotations

from pathlib import Path

import pytest

from .judge import NotStarted, WrongAnswer, load_spec, run_case


def problem_tests(test_file: str):
    spec = load_spec(Path(test_file).resolve().parent)
    timed_out: list[str] = []                     # once a case runs out of time, the rest would only do the same

    @pytest.mark.parametrize("case", spec.cases, ids=[case.name for case in spec.cases])
    def test_case(case, request):
        stress = request.config.getoption("--stress", default=False)
        if case.stress and not stress:
            pytest.skip("stress case: run with --stress")
        if timed_out:
            pytest.skip(f"skipped: '{timed_out[0]}' ran out of time")
        verdict = None
        try:
            run_case(spec, case, stress=stress)
        except NotStarted:
            verdict = "not started"
        except WrongAnswer as wrong:
            verdict = str(wrong)
            if verdict.startswith("Time limit"):
                timed_out.append(case.name)
        # Raised out here, not inside the handlers, so the report is the verdict alone and not a chain of exceptions.
        if verdict == "not started":
            pytest.skip(verdict)
        if verdict is not None:
            pytest.fail(verdict, pytrace=False)      # the input, what was expected, what came back

    return test_case
