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
    assert progress.solves() == {}                                          # a wrong answer is no stroke
    problem(folder, "class Solution:\n    def add(self, a, b): return a + b", ADD)
    judge_and_report(folder)
    first = progress.solves()
    assert first == {"two-sum": 1}
    problem(folder, "class Solution:\n    def add(self, a, b): return a - b", ADD)
    judge_and_report(folder)
    assert progress.solves() == first                                       # a later wrong answer takes nothing away
    capsys.readouterr()
    assert cli.main(["list"]) == 0
    said = capsys.readouterr().out
    assert "─····  001     Two Sum" in said and "1 of 1 solved" in said

    elsewhere = tmp_path / "copies" / "003_merge_two_sorted_lists"; elsewhere.mkdir(parents=True)
    problem(elsewhere, "class Solution:\n    def add(self, a, b): return a + b", ADD)
    judge_and_report(elsewhere)
    assert progress.solves() == {"two-sum": 1}                              # a copy outside the repo does not count


def test_prints_are_shown_with_the_case_they_belong_to(tmp_path):
    from leetkit.run import judge_folder, report
    spec = {**ADD, "cases": [{"name": "one", "args": [1, 1], "expected": 2}, {"name": "two", "args": [2, 2], "expected": 5},
                             {"name": "three", "args": [3, 3], "expected": 6}]}
    folder = problem(tmp_path, "class Solution:\n    def add(self, a, b):\n        print('adding', a)\n        print('and', b)\n        return a + b", spec)
    said = report("Add", judge_folder(folder)).split("\n")
    assert said[0].startswith("Add   Wrong Answer   1 / 3") and "  two" in said
    assert said.index("  Stdout      adding 2") == said.index("              b = 2") + 1          # after the input
    assert said.index("              and 2") + 1 == said.index("  Output      4")               # before the output
    assert not any("adding 1" in row or "adding 3" in row for row in said)                       # only the failing case's

    spec["cases"][1]["expected"] = 4
    folder = problem(tmp_path, "class Solution:\n    def add(self, a, b):\n        print('adding', a)\n        print('and', b)\n        return a + b", spec)
    said = report("Add", judge_folder(folder)).split("\n")
    assert said[0].startswith("Add   Accepted   3 / 3") and said[2:] == ["  one", "  Stdout      adding 1", "              and 1"]

    quiet = problem(tmp_path, "class Solution:\n    def add(self, a, b): return a + b", spec)
    assert len(report("Add", judge_folder(quiet)).split("\n")) == 1                              # no prints, one line

    noisy = problem(tmp_path, "class Solution:\n    def add(self, a, b):\n        for n in range(100): print(n)\n        return 0", spec)
    assert "... and 70 more lines" in report("Add", judge_folder(noisy))


def test_state_kept_on_the_class_leaks_from_case_to_case_as_it_would_on_leetcode(tmp_path):
    from leetkit.run import judge_folder
    spec = {"class": "Bag", "cases": [{"name": "first", "ops": ["Bag", "put", "size"], "args": [[], [1], []], "expected": [None, None, 1]},
                                      {"name": "second", "ops": ["Bag", "put", "size"], "args": [[], [2], []], "expected": [None, None, 1]}]}
    folder = problem(tmp_path, """
        class Bag:
            items = []                                  # shared by every Bag: the slip
            def put(self, x): self.items.append(x)
            def size(self): return len(self.items)
        """, spec)
    result = judge_folder(folder)
    assert (result.verdict, result.case, result.passed) == ("Wrong Answer", "second", 1)


def test_a_stroke_is_earned_by_a_new_solve_not_by_checking_again(tmp_path, monkeypatch, capsys):
    import datetime
    from leetkit import cli, progress
    from leetkit.run import judge_and_report
    monkeypatch.setattr("leetkit.catalog.PROBLEMS_DIR", tmp_path)
    folder = tmp_path / "001_two_sum"; folder.mkdir()
    right = "class Solution:\n    def add(self, a, b): return a + b"
    problem(folder, right, ADD)
    (tmp_path / "stubs").mkdir()

    class Day(datetime.date):
        now = datetime.date(2026, 9, 21)
        @classmethod
        def today(cls): return cls.now
    monkeypatch.setattr(progress, "date", Day)

    judge_and_report(folder); judge_and_report(folder)
    assert progress.solves() == {"two-sum": 1}                              # the same day, the same code: one stroke
    problem(folder, right + "  # tidied", ADD); judge_and_report(folder)
    assert progress.solves() == {"two-sum": 1}                              # the same day, other code: still one
    Day.now = datetime.date(2026, 9, 22)
    judge_and_report(folder)
    assert progress.solves() == {"two-sum": 1}                              # a new day, but the code that already counted
    problem(folder, right + "  # written again", ADD); judge_and_report(folder)
    assert progress.solves() == {"two-sum": 2}                              # a new day and new code: a second stroke
    progress.note_reset("two-sum"); judge_and_report(folder)
    assert progress.solves() == {"two-sum": 3}                              # solved again after a reset, even the same day

    for _ in range(4):
        progress.note_reset("two-sum"); judge_and_report(folder)
    capsys.readouterr()
    assert cli.main(["list"]) == 0
    assert "─│─│─  001     Two Sum" in capsys.readouterr().out                  # seven solves: the five strokes, and no more
    assert cli._strokes(3, terminal=True) == "\033[1;32m─│─\033[0m\033[2m│─\033[0m"


def test_the_older_progress_file_reads_as_one_solve_each(journal_file):
    from leetkit import progress
    import datetime
    progress.PATH.write_text('{"two-sum": "%s", "3sum": "2020-01-01"}' % datetime.date.today().isoformat())
    assert progress.solves() == {"two-sum": 1, "3sum": 1}
    assert progress.mark_solved("two-sum", "abc") is False                  # the same day: nothing new
    assert progress.mark_solved("3sum", "abc") is False                     # an older mark: its code is only put on record
    assert progress.mark_solved("3sum", "abc, written again") is True       # another day, other code: a second stroke
    assert progress.solves() == {"two-sum": 1, "3sum": 2}
