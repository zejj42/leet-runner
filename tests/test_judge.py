"""The judge must be right before it can tell you that you are wrong."""

import json

import pytest

from leetkit import ListNode, TreeNode, linked_list_from_list, linked_list_to_list, tree_from_list, tree_to_list
from leetkit.judge import NotStarted, WrongAnswer, load_spec, run_case

from helpers import ADD, judge, problem


def test_a_right_answer_passes(tmp_path):
    judge(problem(tmp_path, "class Solution:\n    def add(self, a, b): return a + b", ADD))


def test_a_wrong_answer_says_what_was_given_expected_and_got(tmp_path):
    with pytest.raises(WrongAnswer) as wrong:
        judge(problem(tmp_path, "class Solution:\n    def add(self, a, b): return a - b", ADD))
    message = str(wrong.value)
    assert wrong.value.verdict == "Wrong Answer"
    assert "Input       a = 2" in message and "b = 3" in message
    assert "Output      -1" in message and "Expected    5" in message


def test_an_untouched_stub_is_not_started_rather_than_wrong(tmp_path):
    with pytest.raises(NotStarted):
        judge(problem(tmp_path, "class Solution:\n    def add(self, a, b): raise NotImplementedError", ADD))


def test_an_endless_loop_is_stopped(tmp_path):
    spec = {**ADD, "time_limit": 0.2}
    with pytest.raises(WrongAnswer) as wrong:
        judge(problem(tmp_path, "class Solution:\n    def add(self, a, b):\n        while True: pass", spec))
    assert wrong.value.verdict == "Time Limit Exceeded"


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
    spec = {**ADD, "cases": [{"name": "big", "file": "big.json", "large": True}]}
    loaded = load_spec(problem(tmp_path, "class Solution:\n    def add(self, a, b): return a + b", spec))
    assert loaded.cases[0].large and loaded.cases[0].args == [40, 2]
    run_case(loaded, loaded.cases[0])


def test_a_large_case_can_keep_its_data_gzipped(tmp_path):
    import gzip
    spec = {**ADD, "cases": [{"name": "big", "file": "large_input.json.gz", "large": True}]}
    folder = problem(tmp_path, "class Solution:\n    def add(self, a, b): return a + b", spec)
    (folder / "large_input.json.gz").write_bytes(gzip.compress(json.dumps({"args": [40, 2], "expected": 42}).encode()))
    judge(folder)
    assert load_spec(folder).cases[0].args == [40, 2]


def test_list_and_tree_round_trips():
    assert linked_list_to_list(linked_list_from_list([1, 2, 3])) == [1, 2, 3]
    assert linked_list_from_list([]) is None
    for tree in ([], [1], [1, None, 2, 3], [3, 9, 20, None, None, 15, 7], [1, 2, 3, 4, None, None, 5]):
        assert tree_to_list(tree_from_list(tree)) == tree
    assert isinstance(linked_list_from_list([1]), ListNode) and isinstance(tree_from_list([1]), TreeNode)


def test_a_list_that_loops_cannot_hang_the_judge():
    head = linked_list_from_list([1, 2])
    head.next.next = head
    assert linked_list_to_list(head) == [1, 2, "...and back to index 0, in a loop"]
    endless = linked_list_from_list(list(range(80)))
    assert len(linked_list_to_list(endless, limit=50)) == 50


def test_a_cycle_position_shapes_the_list_and_is_not_passed_on(tmp_path):
    spec = {"function": "loops", "params": [{"name": "head", "type": "ListNode"}, {"name": "pos", "type": "cycle position"}],
            "returns": "boolean", "cases": [{"name": "tail to second", "args": [[3, 2, 0, -4], 1], "expected": True},
                                            {"name": "no cycle", "args": [[1, 2], -1], "expected": False},
                                            {"name": "empty", "args": [[], -1], "expected": False}]}
    folder = problem(tmp_path, """
        class Solution:
            def loops(self, head):                      # takes the list alone; reports whether node 4 leads back to node 2
                nodes = []
                while head is not None and len(nodes) < 10:
                    nodes.append(head); head = head.next
                return len(nodes) == 10 and nodes[4] is nodes[1]
        """, spec)
    for index in range(3):
        judge(folder, index)


def test_recursing_down_a_very_long_list_is_allowed_as_on_leetcode(tmp_path):
    spec = {"function": "count", "params": [{"name": "head", "type": "ListNode"}], "returns": "integer",
            "cases": [{"name": "long", "args": [list(range(100_000))], "expected": 100_000}]}
    judge(problem(tmp_path, """
        class Solution:
            def count(self, head):
                return 0 if head is None else 1 + self.count(head.next)
        """, spec))
