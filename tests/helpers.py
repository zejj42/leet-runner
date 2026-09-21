"""What the kit's tests share: a throwaway problem folder, and the judge run on one of its cases."""

import json
import os
import subprocess
import sys
import textwrap
from pathlib import Path

from leetkit.judge import load_spec, run_case


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


QUESTION = {"questionFrontendId": "1", "title": "Two Sum", "difficulty": "Easy", "isPaidOnly": False, "hints": ["Think."],
            "content": "<p>Add.</p><pre>\n<strong>Input:</strong> nums = [1,2], target = 3\n<strong>Output:</strong> [0,1]\n</pre>",
            "metaData": json.dumps({"name": "twoSum", "params": [{"name": "nums", "type": "integer[]"}, {"name": "target", "type": "integer"}],
                                    "return": {"type": "integer[]"}}),
            "exampleTestcaseList": ["[1,2]\n3"],
            "codeSnippets": [{"langSlug": "python3", "code": "class Solution:\n    def twoSum(self, nums: list[int], target: int) -> list[int]:\n        "}]}


def _run_as_script(folder: Path, extra_env: dict | None = None) -> subprocess.CompletedProcess:
    """Runs solution.py the way ▶ does, with the hook installed by hand instead of by the .pth file.
    (The environment's own .pth has already run by then, for "-c", so its once-only guard is reset first.)"""
    root = Path(__file__).resolve().parent.parent
    starter = ("import sys, runpy; sys.argv = [sys.argv[1]]; import leetkit.autorun as a; a._installed = False; a.install(); "
               "runpy.run_path(sys.argv[0], run_name='__main__')")
    return subprocess.run([sys.executable, "-c", starter, str(folder / "solution.py")], capture_output=True, text=True,
                          env={**os.environ, "PYTHONPATH": str(root), **(extra_env or {})})


def _git(folder, *command):
    subprocess.run(["git", "-C", str(folder), "-c", "user.name=t", "-c", "user.email=t@t", *command], check=True, capture_output=True)
