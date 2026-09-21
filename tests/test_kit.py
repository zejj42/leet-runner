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
from leetkit.statement import example_outputs, to_markdown, without_follow_up


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
    spec = {**ADD, "cases": [{"name": "big", "file": "big.json", "large": True}]}
    loaded = load_spec(problem(tmp_path, "class Solution:\n    def add(self, a, b): return a + b", spec))
    assert loaded.cases[0].large and loaded.cases[0].args == [40, 2]
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
    assert linked_list_to_list(head) == [1, 2, "...and back to index 0, in a loop"]
    endless = linked_list_from_list(list(range(80)))
    assert len(linked_list_to_list(endless, limit=50)) == 50


# ---- the catalog

def test_the_whole_list_is_here_and_every_folder_name_is_unique():
    problems = all_problems()
    assert len([p for p in problems if p.number]) == 169
    assert len({p.folder.name for p in problems}) == len(problems)
    assert len({p.slug for p in problems}) == len(problems)


@pytest.mark.parametrize("reference", ["1", "001", "two-sum", "two sum", "Two Sum", "TWO-SUM", "001_two_sum"])
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


def test_statements_become_readable_markdown_without_the_follow_up():
    html = ("<p>Given <code>nums</code>, return <em>it</em>.</p><pre>\n<strong>Input:</strong> nums = [1]\n"
            "<strong>Output:</strong> [1]\n</pre><ul>\n\t<li><code>1 &lt;= n &lt;= 10<sup>4</sup></code></li></ul>"
            "<strong>Follow-up:&nbsp;</strong>Can you do better?")
    statement = without_follow_up(to_markdown(html))
    assert "Given `nums`, return *it*." in statement
    assert "> **Input:** `nums = [1]`" in statement and "> **Output:** `[1]`" in statement      # an example, as a quote
    assert "```" not in statement
    assert "`1 <= n <= 10^4`" in statement
    assert "Follow" not in statement and "do better" not in statement
    assert example_outputs(html) == ["[1]"]


def test_cases_are_written_one_per_line_and_read_back_the_same():
    spec = {"function": "f", "params": [{"name": "a", "type": "integer"}], "returns": "integer", "compare": "exact",
            "cases": [{"name": "one", "args": [1], "expected": 1}, {"name": "two", "args": [2], "expected": 2}]}
    text = format_cases(spec)
    assert json.loads(text) == spec
    assert text.count("\n") == 12


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
    monkeypatch.setattr("leetkit.catalog.STUBS_DIR", tmp_path / "stubs")
    two_sum = find("1")
    folder = scaffolding.scaffold(two_sum)
    assert two_sum.stub.read_text() == (folder / "solution.py").read_text()            # kept for `leet reset`

    solution = (folder / "solution.py").read_text()
    assert "__main__" not in solution and "raise NotImplementedError" in solution      # the hand-run block lives elsewhere
    assert not (folder / "scratch.py").exists()
    assert json.loads((folder / "cases.json").read_text())["cases"][0]["expected"] == [0, 1]
    readme = (folder / "README.md").read_text()
    assert 'class="badge easy"' in readme and "Hint" not in readme and "Follow" not in readme

    (folder / "solution.py").write_text("mine")
    (folder / "cases.json").write_text('{"mine": true}')
    (folder / "README.md").write_text("reworded")
    (folder / "large_input.json").write_text("mine as well")
    two_sum.stub.write_text("stale")
    scaffolding.scaffold(two_sum)                                                       # a second time: fills in, never replaces
    assert (folder / "solution.py").read_text() == "mine"
    assert (folder / "cases.json").read_text() == '{"mine": true}'
    assert (folder / "README.md").read_text() == "reworded"
    assert (folder / "large_input.json").read_text() == "mine as well"
    assert "raise NotImplementedError" in two_sum.stub.read_text()                      # only what comes from the kit is refreshed
    assert sorted(path.name for path in folder.iterdir()) == ["README.md", "cases.json", "large_input.json", "solution.py"]


# ---- pressing ▶ on a solution.py

def _run_as_script(folder: Path, extra_env: dict | None = None) -> subprocess.CompletedProcess:
    """Runs solution.py the way ▶ does, with the hook installed by hand instead of by the .pth file.
    (The environment's own .pth has already run by then, for "-c", so its once-only guard is reset first.)"""
    root = Path(__file__).resolve().parent.parent
    starter = ("import sys, runpy; sys.argv = [sys.argv[1]]; import leetkit.autorun as a; a._installed = False; a.install(); "
               "runpy.run_path(sys.argv[0], run_name='__main__')")
    return subprocess.run([sys.executable, "-c", starter, str(folder / "solution.py")], capture_output=True, text=True,
                          env={**os.environ, "PYTHONPATH": str(root), **(extra_env or {})})


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


def test_judging_stops_at_the_first_case_that_fails_and_counts_what_passed_before_it(tmp_path):
    from leetkit.run import judge_folder
    spec = {**ADD, "cases": [{"name": "one", "args": [1, 1], "expected": 2}, {"name": "two", "args": [2, 2], "expected": 5},
                             {"name": "three", "args": [3, 3], "expected": 7}, {"name": "big", "args": [4, 4], "expected": 8, "large": True}]}
    folder = problem(tmp_path, "class Solution:\n    def add(self, a, b): return a + b", spec)
    result = judge_folder(folder)                                  # the large cases count too, as on LeetCode
    assert (result.verdict, result.passed, result.total, result.case) == ("Wrong Answer", 1, 4, "two")


def test_the_colour_extension_packs_into_something_vs_code_can_install(tmp_path):
    import zipfile
    from leetkit.colours import pack
    names = zipfile.ZipFile(pack(tmp_path / "colours.vsix")).namelist()
    assert {"[Content_Types].xml", "extension.vsixmanifest", "extension/package.json",
            "extension/syntaxes/verdict.tmLanguage.json"} <= set(names)


# ---- the leet command

def test_the_command_takes_a_number_a_slug_or_title_words_and_nothing_else(capsys):
    from leetkit import cli
    for words in (["1"], ["two-sum"], ["Two", "Sum"], ["001_two_sum"]):
        assert cli._in_the_repo(words).slug == "two-sum"
    assert cli.main(["test", "no-such-problem-at-all"]) == 2 and "No problem matches" in capsys.readouterr().err
    assert cli.main(["test", "valid-parentheses"]) in (0, 1, 2)            # on the list; judged once its folder exists
    for gone in (["new", "2"], ["list"], ["next"], ["test"], ["open"]):
        with pytest.raises(SystemExit):
            cli.main(gone)


def test_reset_puts_the_empty_solution_back_but_only_after_a_yes(tmp_path, monkeypatch, capsys):
    from leetkit import cli
    monkeypatch.setattr(scaffolding, "fetch", lambda slug: QUESTION)
    monkeypatch.setattr("leetkit.catalog.PROBLEMS_DIR", tmp_path)
    monkeypatch.setattr("leetkit.catalog.STUBS_DIR", tmp_path / "stubs")
    monkeypatch.setattr("leetkit.cli.ROOT", tmp_path)
    solution = scaffolding.scaffold(find("two-sum")) / "solution.py"
    empty = solution.read_text()

    assert cli.main(["reset", "two-sum"]) == 0 and "already" in capsys.readouterr().out   # nothing to erase, nothing asked

    solution.write_text("my code")
    monkeypatch.setattr("builtins.input", lambda prompt: "")
    assert cli.main(["reset", "two-sum"]) == 1 and solution.read_text() == "my code"      # Enter alone means no
    monkeypatch.setattr("builtins.input", lambda prompt: "y")
    assert cli.main(["reset", "two-sum"]) == 0 and solution.read_text() == empty

    solution.write_text("my code")
    monkeypatch.setattr("builtins.input", lambda prompt: pytest.fail("asked, despite --yes"))
    assert cli.main(["reset", "1", "--yes"]) == 0 and solution.read_text() == empty


def test_every_problem_in_the_repo_can_be_reset():
    from leetkit.catalog import all_problems
    for problem in all_problems():
        if problem.folder.exists():
            assert "raise NotImplementedError" in problem.stub.read_text(), problem.title


# ---- the journal

@pytest.fixture(autouse=True)
def journal_file(tmp_path, monkeypatch):
    """No test writes in the real journal."""
    monkeypatch.setattr("leetkit.journal.PATH", tmp_path / "journal.jsonl")
    return tmp_path / "journal.jsonl"


def test_every_command_is_journalled_whatever_came_of_it(journal_file, tmp_path, monkeypatch):
    from leetkit import cli
    (tmp_path / "add").mkdir()
    folder = problem(tmp_path / "add", "class Solution:\n    def add(self, a, b): return a - b", ADD)
    real = cli._in_the_repo
    added = type("P", (), {"slug": "add", "folder": folder, "title": "Add"})()
    monkeypatch.setattr(cli, "_in_the_repo", lambda words: added if words == ["add"] else real(words))
    assert cli.main(["test", "add"]) == 1
    assert cli.main(["test", "no-such-problem-at-all"]) == 2
    with pytest.raises(SystemExit):
        cli.main(["list"])

    lines = [json.loads(line) for line in journal_file.read_text().splitlines()]
    assert [(line["command"], line["args"], line["exit"]) for line in lines] == [
        ("test", ["add"], 1), ("test", ["no-such-problem-at-all"], 2), ("list", [], 2)]
    assert lines[0]["verdict"] == "Wrong Answer" and (lines[0]["passed"], lines[0]["total"]) == (0, 1)
    assert lines[0]["problem"] == "add" and lines[0]["failed_case"] == "small" and "at" in lines[0]
    assert "No problem matches" in lines[1]["error"]


# ---- what the linked-list problems needed

def test_the_newer_example_markup_reads_like_the_older_one():
    html = ('<p><strong class="example">Example 1:</strong></p>\n<div class="example-block">\n'
            '<p><strong>Input:</strong> <span class="example-io">head = [1,2]</span></p>\n'
            '<p><strong>Output:</strong> <span class="example-io">[2,1]</span></p>\n<p><strong>Explanation:</strong></p>\n'
            '<p><img alt="" src="https://x/y.jpg" /></p>\n</div>\n<p><strong>Constraints:</strong></p>')
    text = to_markdown(html)
    assert "> **Input:** `head = [1,2]`" in text and "> **Output:** `[2,1]`" in text
    assert "Explanation" not in text and "![](https://x/y.jpg)" in text and "**Constraints:**" in text
    assert without_follow_up("the end.** Follow up:** Do better?") == "the end."


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


def test_a_method_holding_only_leetcodes_note_still_counts_as_not_started():
    stub = scaffolding._fill_bodies('class Solution:\n    def go(self, head) -> None:\n        """\n        Do not return anything.\n        """\n        ')
    assert stub.endswith('"""\n        raise NotImplementedError  # your code goes here')
    written = 'class Solution:\n    def go(self):\n        """Mine."""\n        return 1'
    assert scaffolding._fill_bodies(written) == written


def test_recursing_down_a_very_long_list_is_allowed_as_on_leetcode(tmp_path):
    spec = {"function": "count", "params": [{"name": "head", "type": "ListNode"}], "returns": "integer",
            "cases": [{"name": "long", "args": [list(range(100_000))], "expected": 100_000}]}
    judge(problem(tmp_path, """
        class Solution:
            def count(self, head):
                return 0 if head is None else 1 + self.count(head.next)
        """, spec))


@pytest.mark.parametrize("installed, chosen", [({"nvim", "vim"}, "nvim"), ({"vim"}, "vim"), ({"nvim"}, "nvim")])
def test_leet_code_opens_the_solution_in_neovim_or_else_vim_from_inside_its_folder(monkeypatch, journal_file, installed, chosen):
    from leetkit import cli
    started = {}
    monkeypatch.setattr(cli.shutil, "which", lambda name: f"/usr/bin/{name}" if name in installed else None)
    monkeypatch.setattr(cli.subprocess, "call", lambda command, cwd: started.update(command=command, cwd=cwd) or 0)
    assert cli.main(["code", "two", "sum"]) == 0
    assert started == {"command": [chosen, "solution.py"], "cwd": find("two-sum").folder}
    entry = json.loads(journal_file.read_text())
    assert (entry["problem"], entry["editor"]) == ("two-sum", chosen)


def test_leet_code_says_so_when_there_is_no_editor(monkeypatch, capsys):
    from leetkit import cli
    monkeypatch.setattr(cli.shutil, "which", lambda name: None)
    assert cli.main(["code", "two-sum"]) == 2 and "Neither nvim nor vim" in capsys.readouterr().err


# ---- leet update

def _git(folder, *command):
    subprocess.run(["git", "-C", str(folder), "-c", "user.name=t", "-c", "user.email=t@t", *command], check=True, capture_output=True)


def test_update_brings_new_problems_and_leaves_what_you_wrote_alone(tmp_path, monkeypatch, capsys):
    from leetkit import cli
    origin, clone = tmp_path / "origin", tmp_path / "clone"
    (origin / "problems" / "001_two_sum").mkdir(parents=True)
    (origin / ".gitignore").write_text("problems/*/solution.py\n")
    (origin / "problems" / "001_two_sum" / "cases.json").write_text('{\n  "cases": [\n    1\n  ]\n}\n')
    _git(origin, "init", "-q", "-b", "main"); _git(origin, "add", "-A"); _git(origin, "commit", "-qm", "one")
    subprocess.run(["git", "clone", "-q", str(origin), str(clone)], check=True)

    (clone / "problems" / "001_two_sum" / "solution.py").write_text("my code")                       # not in git at all
    (clone / "problems" / "001_two_sum" / "cases.json").write_text('{\n  "cases": [\n    1,\n    "mine"\n  ]\n}\n')
    (origin / "problems" / "003_merge_two_sorted_lists").mkdir()
    (origin / "problems" / "003_merge_two_sorted_lists" / "cases.json").write_text("{}")
    _git(origin, "add", "-A"); _git(origin, "commit", "-qm", "two")

    monkeypatch.setattr(cli, "ROOT", clone)
    monkeypatch.setattr("leetkit.catalog.PROBLEMS_DIR", clone / "problems")
    again = []
    monkeypatch.setattr(cli, "_setup_again", lambda: again.append(True) or 0)
    assert cli.main(["update"]) == 0
    said = capsys.readouterr().out
    assert "Updated  0.0.1 → 0.0.2" in said and "· two" in said and "· Merge Two Sorted Lists     leet read merge-two-sorted-lists" in said and again == [True]
    assert (clone / "problems" / "003_merge_two_sorted_lists" / "cases.json").exists()
    assert (clone / "problems" / "001_two_sum" / "solution.py").read_text() == "my code"
    assert '"mine"' in (clone / "problems" / "001_two_sum" / "cases.json").read_text()

    assert cli.main(["update"]) == 0 and "Already up to date" in capsys.readouterr().out and again == [True]


def test_a_problem_without_a_solution_file_gets_its_empty_stub(tmp_path, monkeypatch):
    from leetkit import cli
    monkeypatch.setattr("leetkit.catalog.PROBLEMS_DIR", tmp_path)
    two_sum = find("two-sum")
    two_sum.folder.mkdir()
    assert cli._in_the_repo(["two-sum"]).slug == "two-sum"
    assert (two_sum.folder / "solution.py").read_text() == two_sum.stub.read_text()
    (two_sum.folder / "solution.py").write_text("mine")
    cli.lay_out_solutions()
    assert (two_sum.folder / "solution.py").read_text() == "mine"


def test_open_says_why_when_vs_code_cannot_open_a_window(monkeypatch, capsys):
    from leetkit import cli
    monkeypatch.setattr(cli.subprocess, "call", lambda command: 0)
    monkeypatch.setattr(cli.shutil, "which", lambda name: "/usr/bin/code")
    monkeypatch.setenv("SSH_CONNECTION", "10.0.0.6 1 10.0.0.12 22")
    monkeypatch.delenv("TERM_PROGRAM", raising=False)
    assert cli.main(["open", "two-sum"]) == 1 and "ssh session" in capsys.readouterr().out
    monkeypatch.setenv("TERM_PROGRAM", "vscode")                  # VS Code's own remote terminal can
    assert cli.main(["open", "two-sum"]) == 0
    monkeypatch.delenv("SSH_CONNECTION")
    monkeypatch.setattr(cli.shutil, "which", lambda name: None)
    assert cli.main(["open", "two-sum"]) == 1 and "leet code two-sum" in capsys.readouterr().out


# ---- leet read

def test_a_statement_is_laid_out_for_the_terminal():
    from leetkit.reader import render
    text = render("# 1. Two Sum\n\n<span class=\"badge easy\">Easy</span> <span class=\"where\">array · First 75</span>\n\n"
                  "<https://leetcode.com/problems/two-sum/>\n\nYou get `nums` and **exactly** one *pair* of them " + "adds up " * 20 + "\n\n"
                  "**Example 1:**\n\n![](https://x/y.png)\n\n> **Input:** `nums = [2,7]`  \n> **Output:** `[0,1]`  \n\n"
                  "```\nL0 → L1\n```\n\n**Constraints:**\n\n - `2 <= nums.length <= 10^4`\n", colour=False, width=60)
    assert text.startswith("1. Two Sum\n\nEasy   array · First 75\n\nhttps://leetcode.com/problems/two-sum/\n")
    assert "You get nums and exactly one pair of them" in text and max(len(row) for row in text.split("\n")) <= 60
    assert "Example 1:\n" in text and "(picture)  https://x/y.png" in text
    assert "  │ Input: nums = [2,7]\n  │ Output: [0,1]" in text
    assert "    L0 → L1" in text and "  • 2 <= nums.length <= 10^4" in text
    assert "*" not in text and "`" not in text and "<" not in text.replace("<=", "")
    assert "\033[1;32mEasy" in render('<span class="badge easy">Easy</span>', colour=True)


def test_every_statement_in_the_repo_can_be_read(capsys):
    from leetkit import cli
    from leetkit.catalog import all_problems
    for problem in all_problems():
        if problem.folder.exists():
            assert cli.main(["read", problem.slug]) == 0
            said = capsys.readouterr().out
            assert problem.title in said and "**" not in said and "<span" not in said, problem.title
