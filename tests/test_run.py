"""Judging a whole folder: the verdict, ▶ on a solution.py, and what gets noted as solved."""

import os
import subprocess
import sys
from pathlib import Path

from helpers import ADD, problem, _run_as_script


def test_judging_stops_at_the_first_case_that_fails_and_counts_what_passed_before_it(tmp_path):
    from leetkit.run import judge_folder
    spec = {**ADD, "cases": [{"name": "one", "args": [1, 1], "expected": 2}, {"name": "two", "args": [2, 2], "expected": 5},
                             {"name": "three", "args": [3, 3], "expected": 7}, {"name": "big", "args": [4, 4], "expected": 8, "large": True}]}
    folder = problem(tmp_path, "class Solution:\n    def add(self, a, b): return a + b", spec)
    result = judge_folder(folder)                                  # the large cases count too, as on LeetCode
    assert (result.verdict, result.passed, result.total, result.case) == ("Wrong Answer", 1, 4, "two")


def test_running_a_solution_file_judges_it(tmp_path):
    folder = problem(tmp_path, "class Solution:\n    def add(self, a, b): return a + b", ADD)
    run = _run_as_script(folder)
    assert "Accepted   1 / 1 testcases passed" in run.stdout and len(run.stdout.splitlines()) == 1
    assert "small" not in run.stdout                               # like LeetCode: no list of what passed

    folder = problem(tmp_path, "class Solution:\n    def add(self, a, b): return a - b", ADD)
    run = _run_as_script(folder)
    assert "Wrong Answer   0 / 1 testcases passed" in run.stdout
    assert "Output      -1" in run.stdout and "Expected    5" in run.stdout


def test_a_crash_is_reported_with_its_line_in_your_file(tmp_path):
    folder = problem(tmp_path, "class Solution:\n    def add(self, a, b):\n        return a / 0", ADD)
    out = _run_as_script(folder).stdout
    assert "Runtime Error   0 / 1 testcases passed" in out and "ZeroDivisionError: division by zero     line 3" in out
    assert "Last input  a = 2" in out


def test_other_files_are_left_alone(tmp_path):
    from leetkit import autorun
    (tmp_path / "other.py").write_text("print('hello')")
    (tmp_path / "cases.json").write_text("{}")
    run = subprocess.run([sys.executable, "-c", "import sys; sys.argv=[sys.argv[1]]; import leetkit.autorun as a; a._installed = False; a.install(); "
                          "import atexit; print('hooks', atexit._ncallbacks())", str(tmp_path / "other.py")],
                         capture_output=True, text=True, env={**os.environ, "PYTHONPATH": str(Path(__file__).resolve().parent.parent)})
    assert "hooks 0" in run.stdout, run.stdout + run.stderr


def test_an_accepted_problem_is_marked_solved_in_the_list_and_stays_so(tmp_path, monkeypatch, capsys):
    from leetkit import cli, progress
    from leetkit.run import judge_and_report
    monkeypatch.setattr("leetkit.catalog.PROBLEMS_DIR", tmp_path)
    folder = tmp_path / "001_two_sum"; folder.mkdir()
    problem(folder, "class Solution:\n    def add(self, a, b): return a - b", ADD)
    judge_and_report(folder)
    assert progress.solved() == {}                                          # a wrong answer is no note
    problem(folder, "class Solution:\n    def add(self, a, b): return a + b", ADD)
    judge_and_report(folder)
    first = progress.solved()
    assert list(first) == ["two-sum"]
    problem(folder, "class Solution:\n    def add(self, a, b): return a - b", ADD)
    judge_and_report(folder)
    assert progress.solved() == first                                       # solved stays solved
    capsys.readouterr()
    assert cli.main(["list"]) == 0
    said = capsys.readouterr().out
    assert "✓ 001  Two Sum" in said and "1 of 1 solved" in said

    elsewhere = tmp_path / "copies" / "003_merge_two_sorted_lists"; elsewhere.mkdir(parents=True)
    problem(elsewhere, "class Solution:\n    def add(self, a, b): return a + b", ADD)
    judge_and_report(elsewhere)
    assert list(progress.solved()) == ["two-sum"]                           # a copy outside the repo does not count
