"""Runs a solution against the cases in a problem's cases.json, the way LeetCode's judge would.

cases.json, for a function problem:

    {
      "function": "twoSum",
      "params": [{"name": "nums", "type": "integer[]"}, {"name": "target", "type": "integer"}],
      "returns": "integer[]",
      "compare": "unordered",
      "cases": [{"name": "example 1", "args": [[2, 7, 11, 15], 9], "expected": [0, 1]}]
    }

"compare" is one of: exact (default), unordered, unordered_nested, float, any_of.
A case may carry "stress": true; those only run with --stress.
A case may be {"name": ..., "file": "big.json", "stress": true}, with its args and expected in that file.
"returns": "void" with "output_param": 0 judges the argument the solution changed in place.
Types ListNode and TreeNode are built from, and turned back into, LeetCode's list notation.

For a class problem (LRU Cache, Min Stack...) use "class": "LRUCache" instead of "function", and cases of
{"ops": ["LRUCache", "put", "get"], "args": [[2], [1, 1], [1]], "expected": [null, null, 1]}.

If a problem has many right answers, put a check.py beside it with
    def check(args: dict, result, expected) -> bool | str      # a str is the reason it is wrong
"""

from __future__ import annotations

import copy
import json
import signal
import threading
import types
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from .structures import linked_list_from_list, linked_list_to_list, tree_from_list, tree_to_list


class NotStarted(Exception):
    """The solution still raises NotImplementedError: nothing to judge yet."""


class WrongAnswer(AssertionError):
    """A case that did not pass. `verdict` is LeetCode's name for why: Wrong Answer, Time Limit Exceeded."""

    def __init__(self, message: str, verdict: str = "Wrong Answer"):
        super().__init__(message)
        self.verdict = verdict


@dataclass(repr=False)
class Case:
    name: str
    args: list
    expected: Any
    stress: bool = False
    ops: Optional[list] = None

    def __repr__(self) -> str:
        return f"Case({self.name!r})"


@dataclass(repr=False)
class Spec:
    folder: Path
    function: Optional[str] = None
    class_name: Optional[str] = None
    params: list = field(default_factory=list)
    returns: str = ""
    compare: str = "exact"
    output_param: Optional[int] = None
    time_limit: float = 2.0
    cases: list = field(default_factory=list)

    @property
    def title(self) -> str:
        return self.folder.name

    def __repr__(self) -> str:
        return f"Spec({self.folder.name!r}, {len(self.cases)} cases)"


def load_spec(folder: Path) -> Spec:
    data = json.loads((folder / "cases.json").read_text())
    cases = []
    for i, c in enumerate(data.get("cases", [])):
        if "file" in c:                                   # a case too big to read keeps its data in its own file
            c = {**json.loads((folder / c["file"]).read_text()), **{k: v for k, v in c.items() if k != "file"}}
        cases.append(Case(name=c.get("name", f"case {i + 1}"), args=c.get("args", []), expected=c.get("expected"),
                          stress=c.get("stress", False), ops=c.get("ops")))
    return Spec(folder=folder, function=data.get("function"), class_name=data.get("class"), params=data.get("params", []),
                returns=data.get("returns", ""), compare=data.get("compare", "exact"), output_param=data.get("output_param"),
                time_limit=data.get("time_limit", 2.0), cases=cases)


# ---- loading the solution

def _load_module(path: Path, name: str):
    """Compiled from the source every time. Python's bytecode cache goes by size and whole-second timestamps,
    so a quick edit of the same length could otherwise be judged as the code it replaced."""
    module = types.ModuleType(name)
    module.__file__ = str(path)
    exec(compile(path.read_text(), str(path), "exec"), module.__dict__)
    return module


# ---- arguments in, results out

def _build(value: Any, type_name: str) -> Any:
    if type_name == "ListNode":
        return linked_list_from_list(value)
    if type_name == "TreeNode":
        return tree_from_list(value)
    if type_name in ("ListNode[]", "list<ListNode>"):
        return [linked_list_from_list(v) for v in value]
    return copy.deepcopy(value)


def _flatten(value: Any, type_name: str) -> Any:
    if type_name == "ListNode":
        return linked_list_to_list(value)
    if type_name == "TreeNode":
        return tree_to_list(value)
    if type_name in ("ListNode[]", "list<ListNode>"):
        return [linked_list_to_list(v) for v in value]
    return value


# ---- comparing

def _sorted_safely(items: list) -> list:
    try:
        return sorted(items)
    except TypeError:
        return sorted(items, key=repr)


def _matches(result: Any, expected: Any, mode: str) -> bool:
    if mode == "unordered":
        return isinstance(result, (list, tuple)) and _sorted_safely(list(result)) == _sorted_safely(list(expected))
    if mode == "unordered_nested":
        if not isinstance(result, (list, tuple)):
            return False
        return (_sorted_safely([_sorted_safely(list(r)) for r in result])
                == _sorted_safely([_sorted_safely(list(e)) for e in expected]))
    if mode == "float":
        return isinstance(result, (int, float)) and abs(result - expected) <= 1e-5
    if mode == "any_of":
        return any(result == option for option in expected)
    if isinstance(result, tuple):
        result = list(result)
    return result == expected


# ---- a time limit, so an endless loop fails instead of hanging

class _TimeLimit:
    def __init__(self, seconds: float):
        self.seconds = seconds
        self.usable = threading.current_thread() is threading.main_thread() and hasattr(signal, "setitimer")

    def __enter__(self):
        if self.usable:
            def on_alarm(signum, frame):
                raise TimeoutError
            self.previous = signal.signal(signal.SIGALRM, on_alarm)
            signal.setitimer(signal.ITIMER_REAL, self.seconds)

    def __exit__(self, *exc):
        if self.usable:
            signal.setitimer(signal.ITIMER_REAL, 0)
            signal.signal(signal.SIGALRM, self.previous)
        return False


# ---- reporting

def _show(value: Any, limit: int = 300) -> str:
    text = json.dumps(value) if isinstance(value, (list, dict, str, int, float, bool, type(None))) else repr(value)
    return text if len(text) <= limit else f"{text[:limit]}… ({len(text)} characters)"


def describe(spec: Spec, case: Case, got: Any = None, show_got: bool = False, note: str = "",
             input_label: str = "Input") -> str:
    """The block LeetCode shows under a verdict: the input, your output, what was expected."""
    if case.ops is not None:
        inputs = [f"ops = {_show(case.ops)}", f"args = {_show(case.args)}"]
    else:
        inputs = [f"{param['name']} = {_show(value)}" for param, value in zip(spec.params, case.args)]
    lines = [f"  {input_label if index == 0 else '':<12}{text}" for index, text in enumerate(inputs)]
    if show_got:
        lines.append(f"  {'Output':<12}{_show(got)}")
    lines.append(f"  {'Expected':<12}{_show(case.expected)}")
    if note:
        lines.append(f"  {'Note':<12}{note}")
    return "\n".join(lines)


# ---- judging one case

def run_case(spec: Spec, case: Case, stress: bool = False) -> None:
    """Raises NotStarted, WrongAnswer or TimeoutError; returns quietly when the case passes."""
    __tracebackhide__ = True
    module = _load_module(spec.folder / "solution.py", f"solution_{spec.folder.name}")
    limit = spec.time_limit * (5 if case.stress else 1)
    try:
        with _TimeLimit(limit):
            result, arguments = (_run_class if spec.class_name else _run_function)(spec, case, module)
    except NotImplementedError:
        raise NotStarted(spec.title) from None
    except TimeoutError:
        raise WrongAnswer(describe(spec, case, note=f"stopped after {limit:g} seconds"), "Time Limit Exceeded") from None

    checker = spec.folder / "check.py"
    if checker.exists():
        verdict = _load_module(checker, f"check_{spec.folder.name}").check(arguments, result, case.expected)
        if verdict is not True:
            raise WrongAnswer(describe(spec, case, result, show_got=True, note=verdict if isinstance(verdict, str) else ""))
    elif not _matches(result, case.expected, spec.compare):
        raise WrongAnswer(describe(spec, case, result, show_got=True))


def _run_function(spec: Spec, case: Case, module) -> tuple[Any, dict]:
    __tracebackhide__ = True
    types = [p.get("type", "") for p in spec.params] + [""] * len(case.args)
    built = [_build(value, types[i]) for i, value in enumerate(case.args)]
    returned = getattr(module.Solution(), spec.function)(*built)
    if spec.output_param is not None:                      # judged on what it did to its argument
        result = _flatten(built[spec.output_param], types[spec.output_param])
    else:
        result = _flatten(returned, spec.returns)
    names = [p["name"] for p in spec.params]
    return result, dict(zip(names, case.args))


def _run_class(spec: Spec, case: Case, module) -> tuple[Any, dict]:
    __tracebackhide__ = True
    instance, results = None, []
    for op, arguments in zip(case.ops, case.args):
        if op == spec.class_name:
            instance = getattr(module, spec.class_name)(*copy.deepcopy(arguments))
            results.append(None)
        else:
            results.append(getattr(instance, op)(*copy.deepcopy(arguments)))
    return results, {"ops": case.ops, "args": case.args}
