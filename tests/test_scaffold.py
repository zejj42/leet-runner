"""Making a problem's folder from what LeetCode serves."""

import json

from leetkit import scaffold as scaffolding
from leetkit.catalog import find
from leetkit.scaffold import _fill_bodies, format_cases

from helpers import QUESTION


def test_empty_methods_get_a_not_started_body_and_written_ones_are_left_alone():
    code = "class MinStack:\n\n    def __init__(self):\n        \n\n    def push(self, val: int) -> None:\n        \n\n    def top(self) -> int:\n        return 1\n"
    filled = _fill_bodies(code)
    assert filled.count("raise NotImplementedError") == 2
    assert "return 1" in filled
    compile(filled, "stub", "exec")


def test_a_method_holding_only_leetcodes_note_still_counts_as_not_started():
    stub = scaffolding._fill_bodies('class Solution:\n    def go(self, head) -> None:\n        """\n        Do not return anything.\n        """\n        ')
    assert stub.endswith('"""\n        raise NotImplementedError  # your code goes here')
    written = 'class Solution:\n    def go(self):\n        """Mine."""\n        return 1'
    assert scaffolding._fill_bodies(written) == written


def test_a_class_stub_ends_with_its_last_method():
    code = "class MinStack:\n\n    def __init__(self):\n        \n\n    def top(self) -> int:\n        \n\n\n# Your MinStack object will be called as such:\n# obj = MinStack()\n"
    stub = scaffolding._fill_bodies(scaffolding._drop_leading_comments(code))
    assert "# Your" not in stub and stub.count("raise NotImplementedError") == 2


def test_cases_are_written_one_per_line_and_read_back_the_same():
    spec = {"function": "f", "params": [{"name": "a", "type": "integer"}], "returns": "integer", "compare": "exact",
            "cases": [{"name": "one", "args": [1], "expected": 1}, {"name": "two", "args": [2], "expected": 2}]}
    text = format_cases(spec)
    assert json.loads(text) == spec
    assert text.count("\n") == 12


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
