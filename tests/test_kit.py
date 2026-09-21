"""Tests of the kit itself: the judge must be right before it can tell you that you are wrong."""

import json
import os
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

from leetkit import ListNode, TreeNode, linked_list_from_list, linked_list_to_list, tree_from_list, tree_to_list
from leetkit.catalog import all_problems, find
from leetkit.judge import NotStarted, WrongAnswer, load_spec, run_case
from leetkit import scaffold as scaffolding
from leetkit.scaffold import _fill_bodies, format_cases
from leetkit.statement import example_outputs, split_follow_up, to_markdown


def problem(tmp_path: Path, solution: str, spec: dict, check: str | None = None) -> Path:
    (tmp_path / "solution.py").write_text(textwrap.dedent(solution))
    (tmp_path / "cases.json").write_text(json.dumps(spec))
    if check:
        (tmp_path / "check.py").write_text(textwrap.dedent(check))
    return tmp_path


def judge(folder: Path, index: int = 0):
    spec = load_spec(folder)
    run_case(spec, spec.cases[index])


ADD = {"function": "add", "params": [{"name": "a", "type": "integer"}, {"name": "b", "type": "integer"}],
       "returns": "integer", "cases": [{"name": "small", "args": [2, 3], "expected": 5}]}


# ---- verdicts

def test_a_right_answer_passes(tmp_path):
    judge(problem(tmp_path, "class Solution:\n    def add(self, a, b): return a + b", ADD))


def test_a_wrong_answer_says_what_was_given_expected_and_got(tmp_path):
    with pytest.raises(WrongAnswer) as wrong:
        judge(problem(tmp_path, "class Solution:\n    def add(self, a, b): return a - b", ADD))
    message = str(wrong.value)
    assert "a = 2" in message and "b = 3" in message and "expected   5" in message and "got        -1" in message


def test_an_untouched_stub_is_not_started_rather_than_wrong(tmp_path):
    with pytest.raises(NotStarted):
        judge(problem(tmp_path, "class Solution:\n    def add(self, a, b): raise NotImplementedError", ADD))


def test_an_endless_loop_is_stopped(tmp_path):
    spec = {**ADD, "time_limit": 0.2}
    with pytest.raises(WrongAnswer, match="Time limit"):
        judge(problem(tmp_path, "class Solution:\n    def add(self, a, b):\n        while True: pass", spec))


def test_a_crash_in_the_solution_surfaces_as_itself(tmp_path):
    with pytest.raises(ZeroDivisionError):
        judge(problem(tmp_path, "class Solution:\n    def add(self, a, b): return 1 / 0", ADD))


def test_the_solution_cannot_spoil_the_case_by_changing_its_arguments(tmp_path):
    spec = {"function": "first", "params": [{"name": "nums", "type": "integer[]"}], "returns": "integer",
            "cases": [{"args": [[3, 1, 2]], "expected": 1}]}
    folder = problem(tmp_path, "class Solution:\n    def first(self, nums):\n        nums.sort()\n        return nums[0]", spec)
    loaded = load_spec(folder)
    run_case(loaded, loaded.cases[0])
    assert loaded.cases[0].args == [[3, 1, 2]]


# ---- ways of comparing

@pytest.mark.parametrize("mode, returned, expected, passes", [
    ("exact", "[1, 0]", [0, 1], False),
    ("unordered", "[1, 0]", [0, 1], True),
    ("unordered", "[1, 1]", [0, 1], False),
    ("unordered_nested", "[[2, 1], [4, 3]]", [[3, 4], [1, 2]], True),
    ("float", "0.3000001", 0.3, True),
    ("any_of", "'bab'", ["bab", "aba"], True),
    ("any_of", "'abb'", ["bab", "aba"], False),
    ("exact", "(0, 1)", [0, 1], True),                # a tuple is as good as a list
])
def test_compare_modes(tmp_path, mode, returned, expected, passes):
    spec = {"function": "f", "params": [], "returns": "", "compare": mode, "cases": [{"args": [], "expected": expected}]}
    folder = problem(tmp_path, f"class Solution:\n    def f(self): return {returned}", spec)
    if passes:
        judge(folder)
    else:
        with pytest.raises(WrongAnswer):
            judge(folder)


def test_a_check_file_decides_when_many_answers_are_right(tmp_path):
    spec = {"function": "f", "params": [{"name": "n", "type": "integer"}], "returns": "integer",
            "cases": [{"args": [10], "expected": None}]}
    check = "def check(args, result, expected):\n    return True if result % 2 == 0 else 'must be even'"
    judge(problem(tmp_path, "class Solution:\n    def f(self, n): return 4", spec, check))
    with pytest.raises(WrongAnswer, match="must be even"):
        judge(problem(tmp_path, "class Solution:\n    def f(self, n): return 5", spec, check))


# ---- kinds of problem

def test_linked_lists_go_in_and_come_out_as_lists(tmp_path):
    spec = {"function": "rev", "params": [{"name": "head", "type": "ListNode"}], "returns": "ListNode",
            "cases": [{"args": [[1, 2, 3]], "expected": [3, 2, 1]}, {"args": [[]], "expected": []}]}
    solution = """
        class Solution:
            def rev(self, head):
                previous = None
                while head:
                    head.next, previous, head = previous, head, head.next
                return previous
    """
    folder = problem(tmp_path, solution, spec)
    judge(folder, 0)
    judge(folder, 1)


def test_trees_go_in_and_come_out_as_lists(tmp_path):
    spec = {"function": "same", "params": [{"name": "root", "type": "TreeNode"}], "returns": "TreeNode",
            "cases": [{"args": [[1, None, 2, 3]], "expected": [1, None, 2, 3]}]}
    judge(problem(tmp_path, "class Solution:\n    def same(self, root): return root", spec))


def test_in_place_problems_are_judged_on_the_argument(tmp_path):
    spec = {"function": "zero", "params": [{"name": "nums", "type": "integer[]"}], "returns": "void", "output_param": 0,
            "cases": [{"args": [[1, 2]], "expected": [0, 0]}]}
    judge(problem(tmp_path, "class Solution:\n    def zero(self, nums):\n        nums[:] = [0] * len(nums)", spec))


def test_class_problems_replay_their_operations(tmp_path):
    spec = {"class": "Counter", "cases": [{"ops": ["Counter", "add", "add", "total"], "args": [[10], [1], [2], []],
                                           "expected": [None, None, None, 13]}]}
    solution = """
        class Counter:
            def __init__(self, start): self.value = start
            def add(self, n): self.value += n
            def total(self): return self.value
    """
    judge(problem(tmp_path, solution, spec))


def test_a_big_case_can_live_in_its_own_file(tmp_path):
    (tmp_path / "big.json").write_text(json.dumps({"args": [40, 2], "expected": 42}))
    spec = {**ADD, "cases": [{"name": "big", "file": "big.json", "stress": True}]}
    loaded = load_spec(problem(tmp_path, "class Solution:\n    def add(self, a, b): return a + b", spec))
    assert loaded.cases[0].stress and loaded.cases[0].args == [40, 2]
    run_case(loaded, loaded.cases[0])


# ---- node types

def test_list_and_tree_round_trips():
    assert linked_list_to_list(linked_list_from_list([1, 2, 3])) == [1, 2, 3]
    assert linked_list_from_list([]) is None
    for tree in ([], [1], [1, None, 2, 3], [3, 9, 20, None, None, 15, 7], [1, 2, 3, 4, None, None, 5]):
        assert tree_to_list(tree_from_list(tree)) == tree
    assert isinstance(linked_list_from_list([1]), ListNode) and isinstance(tree_from_list([1]), TreeNode)


def test_a_list_that_loops_cannot_hang_the_judge():
    head = linked_list_from_list([1, 2])
    head.next.next = head
    assert len(linked_list_to_list(head, limit=50)) == 50


# ---- the catalog

def test_the_whole_list_is_here_and_every_folder_name_is_unique():
    problems = all_problems()
    assert len([p for p in problems if p.number]) == 169
    assert len({p.folder.name for p in problems}) == len(problems)
    assert len({p.slug for p in problems}) == len(problems)


@pytest.mark.parametrize("reference", ["1", "001", "two-sum", "two sum", "Two Sum", "problems/001_two_sum",
                                       "problems/001_two_sum/solution.py", "001_two_sum"])
def test_a_problem_can_be_named_many_ways(reference):
    assert find(reference).slug == "two-sum"


def test_off_list_problems_are_found_by_their_leetcode_id():
    assert find("lc904").slug == "fruit-into-baskets"


def test_an_ambiguous_or_unknown_name_says_so():
    with pytest.raises(LookupError, match="several"):
        find("tree")
    with pytest.raises(LookupError, match="No problem"):
        find("no such problem anywhere")


# ---- scaffolding

def test_empty_methods_get_a_not_started_body_and_written_ones_are_left_alone():
    code = "class MinStack:\n\n    def __init__(self):\n        \n\n    def push(self, val: int) -> None:\n        \n\n    def top(self) -> int:\n        return 1\n"
    filled = _fill_bodies(code)
    assert filled.count("raise NotImplementedError") == 2
    assert "return 1" in filled
    compile(filled, "stub", "exec")


def test_statements_become_readable_markdown_with_the_follow_up_set_aside():
    html = ("<p>Given <code>nums</code>, return <em>it</em>.</p><pre>\n<strong>Input:</strong> nums = [1]\n"
            "<strong>Output:</strong> [1]\n</pre><ul>\n\t<li><code>1 &lt;= n &lt;= 10<sup>4</sup></code></li></ul>"
            "<strong>Follow-up:&nbsp;</strong>Can you do better?")
    statement, follow_up = split_follow_up(to_markdown(html))
    assert "Given `nums`, return *it*." in statement
    assert "> **Input:** `nums = [1]`" in statement and "> **Output:** `[1]`" in statement      # an example, as a quote
    assert "```" not in statement
    assert "`1 <= n <= 10^4`" in statement
    assert "Follow" not in statement and follow_up == "Can you do better?"
    assert example_outputs(html) == ["[1]"]


def test_cases_are_written_one_per_line_and_read_back_the_same():
    spec = {"function": "f", "params": [{"name": "a", "type": "integer"}], "returns": "integer", "compare": "exact",
            "cases": [{"name": "one", "args": [1], "expected": 1}, {"name": "two", "args": [2], "expected": 2}]}
    text = format_cases(spec)
    assert json.loads(text) == spec
    assert text.count("\n") == 12


# ---- many problems side by side

def test_problems_can_all_name_their_test_file_the_same(tmp_path):
    """Every folder has a test_solution.py. Collected together they must not be mistaken for one another."""
    root = Path(__file__).resolve().parent.parent
    for name, answer in (("001_first", 1), ("002_second", 2)):
        folder = tmp_path / name
        folder.mkdir()
        (folder / "solution.py").write_text(f"class Solution:\n    def f(self): return {answer}\n")
        (folder / "cases.json").write_text(json.dumps({"function": "f", "params": [], "returns": "integer",
                                                       "cases": [{"args": [], "expected": answer}]}))
        (folder / "test_solution.py").write_text("from leetkit import problem_tests\n\ntest_case = problem_tests(__file__)\n")
    run = subprocess.run([sys.executable, "-m", "pytest", str(tmp_path), "-c", str(root / "pyproject.toml"), "-q"],
                         capture_output=True, text=True, env={**os.environ, "PYTHONPATH": str(root)})
    assert run.returncode == 0, run.stdout + run.stderr
    assert run.stdout.strip().startswith("..")           # quiet mode: one dot per passing case, and there are two


def test_a_block_that_is_not_an_example_stays_a_code_block():
    assert "```\n  1\n / \\\n2   3\n```" in to_markdown("<pre>\n  1\n / \\\n2   3\n</pre>")


QUESTION = {"questionFrontendId": "1", "title": "Two Sum", "difficulty": "Easy", "isPaidOnly": False, "hints": ["Think."],
            "content": "<p>Add.</p><pre>\n<strong>Input:</strong> nums = [1,2], target = 3\n<strong>Output:</strong> [0,1]\n</pre>",
            "metaData": json.dumps({"name": "twoSum", "params": [{"name": "nums", "type": "integer[]"}, {"name": "target", "type": "integer"}],
                                    "return": {"type": "integer[]"}}),
            "exampleTestcaseList": ["[1,2]\n3"],
            "codeSnippets": [{"langSlug": "python3", "code": "class Solution:\n    def twoSum(self, nums: list[int], target: int) -> list[int]:\n        "}]}


def test_scaffolding_never_overwrites_what_you_may_have_written(tmp_path, monkeypatch):
    monkeypatch.setattr(scaffolding, "fetch", lambda slug: QUESTION)
    monkeypatch.setattr("leetkit.catalog.PROBLEMS_DIR", tmp_path)
    two_sum = find("1")
    folder = scaffolding.scaffold(two_sum)

    solution = (folder / "solution.py").read_text()
    assert "__main__" not in solution and "raise NotImplementedError" in solution      # the hand-run block lives elsewhere
    assert "from solution import Solution" in (folder / "scratch.py").read_text()
    assert json.loads((folder / "cases.json").read_text())["cases"][0]["expected"] == [0, 1]
    assert 'class="badge easy"' in (folder / "README.md").read_text()

    with pytest.raises(FileExistsError):
        scaffolding.scaffold(two_sum)

    (folder / "solution.py").write_text("mine")
    (folder / "cases.json").write_text('{"mine": true}')
    (folder / "scratch.py").write_text("mine too")
    (folder / "README.md").write_text("stale")
    scaffolding.scaffold(two_sum, force=True)
    assert (folder / "solution.py").read_text() == "mine"
    assert (folder / "cases.json").read_text() == '{"mine": true}'
    assert (folder / "scratch.py").read_text() == "mine too"
    assert (folder / "README.md").read_text() != "stale"                                # only what comes from LeetCode is refreshed
