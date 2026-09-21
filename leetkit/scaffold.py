"""Creates a problem's folder: the statement, a stub to write in, the example cases, and a test file.

Everything comes from LeetCode's public API. Nothing here ever writes a solution.
"""

from __future__ import annotations

import json
import re
import urllib.request
from pathlib import Path
from typing import Any, Optional

from .catalog import Problem
from .statement import example_outputs, split_follow_up, to_markdown

_QUERY = """query q($titleSlug: String!) { question(titleSlug: $titleSlug) {
  questionFrontendId title difficulty isPaidOnly content hints metaData exampleTestcaseList
  codeSnippets { langSlug code } } }"""

_STUB_BODY = "raise NotImplementedError  # your code goes here"


def fetch(slug: str) -> dict:
    request = urllib.request.Request(
        "https://leetcode.com/graphql",
        data=json.dumps({"query": _QUERY, "variables": {"titleSlug": slug}}).encode(),
        headers={"Content-Type": "application/json", "Referer": f"https://leetcode.com/problems/{slug}/",
                 "User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        question = json.load(response)["data"]["question"]
    if question is None:
        raise LookupError(f"LeetCode has no problem with the slug '{slug}'")
    return question


def scaffold(problem: Problem, force: bool = False) -> Path:
    folder = problem.folder
    if (folder / "solution.py").exists() and not force:
        raise FileExistsError(f"{folder.name} already exists. Your solution.py is never overwritten.")
    question = fetch(problem.slug)
    meta = json.loads(question.get("metaData") or "{}")
    folder.mkdir(parents=True, exist_ok=True)

    (folder / "README.md").write_text(_readme(problem, question))
    (folder / "cases.json").write_text(format_cases(_cases(question, meta)))
    (folder / "test_solution.py").write_text(_TEST_FILE)
    if not (folder / "solution.py").exists():                  # with --force, everything but your code is refreshed
        (folder / "solution.py").write_text(_stub(problem, question, meta))
    return folder


# ---- README

def _readme(problem: Problem, question: dict) -> str:
    lines = [f"# {question['questionFrontendId']}. {question['title']}", "",
             f"{question['difficulty']} · {problem.topic} · {problem.list}"
             + (f" · {problem.section}" if problem.section else ""), "", f"<{problem.url}>", ""]
    if question.get("isPaidOnly") or not question.get("content"):
        lines += ["This one is for LeetCode subscribers, so its statement could not be fetched. Paste it here.", ""]
    else:
        statement, follow_up = split_follow_up(to_markdown(question["content"]))
        lines += [statement, ""]
        if follow_up:
            lines += ["<details><summary>Follow-up</summary>", "", follow_up, "", "</details>", ""]
    for index, hint in enumerate(question.get("hints") or [], start=1):
        lines += [f"<details><summary>Hint {index}</summary>", "", to_markdown(hint), "", "</details>", ""]
    return "\n".join(lines)


# ---- cases.json

def _cases(question: dict, meta: dict) -> dict:
    params = [{"name": p["name"], "type": p["type"]} for p in meta.get("params", [])]
    outputs = example_outputs(question.get("content") or "")
    cases = []
    for index, raw in enumerate(question.get("exampleTestcaseList") or []):
        values = [_parse(line) for line in raw.split("\n")]
        expected = _parse(outputs[index]) if index < len(outputs) else None
        cases.append({"name": f"example {index + 1}", "args": values, "expected": expected})

    if "classname" in meta:                                     # a class to design: ops and their arguments
        spec: dict[str, Any] = {"class": meta["classname"], "compare": "exact", "cases": [
            {"name": case["name"], "ops": case["args"][0], "args": case["args"][1] if len(case["args"]) > 1 else [],
             "expected": case["expected"]} for case in cases]}
        return spec

    returns = (meta.get("return") or {}).get("type", "")
    spec = {"function": meta.get("name", "solve"), "params": params, "returns": returns, "compare": "exact", "cases": cases}
    if returns == "void":
        spec["output_param"] = (meta.get("output") or {}).get("paramindex", 0)
    return spec


def format_cases(spec: dict) -> str:
    """cases.json laid out for a person: one parameter per line, one case per line."""
    lines = ["{"]
    for key, value in spec.items():
        if key in ("params", "cases"):
            lines.append(f'  "{key}": [')
            lines += [f"    {json.dumps(item, ensure_ascii=False)}," for item in value]
            if value:
                lines[-1] = lines[-1].rstrip(",")
            lines.append("  ],")
        else:
            lines.append(f'  "{key}": {json.dumps(value, ensure_ascii=False)},')
    lines[-1] = lines[-1].rstrip(",")
    return "\n".join(lines + ["}"]) + "\n"


def _parse(text: str) -> Any:
    try:
        return json.loads(text)
    except (ValueError, TypeError):
        return text


# ---- solution.py

def _stub(problem: Problem, question: dict, meta: dict) -> str:
    snippet = next((s["code"] for s in question.get("codeSnippets") or [] if s["langSlug"] == "python3"), None)
    if snippet is None:
        snippet = "class Solution:\n    def solve(self):\n        "
    uses_nodes = [name for name in ("ListNode", "TreeNode") if name in snippet]
    snippet = _fill_bodies(_drop_leading_comments(snippet))

    header = [f'"""{question["questionFrontendId"]}. {question["title"]}  ({question["difficulty"]})', problem.url, '"""', ""]
    typing_names = [name for name in ("List", "Optional", "Dict", "Set", "Tuple") if re.search(rf"\b{name}\[", snippet)]
    if typing_names:
        header.append(f"from typing import {', '.join(typing_names)}")
    if uses_nodes:
        header.append(f"from leetkit import {', '.join(uses_nodes)}")
    while header and not header[-1]:
        header.pop()
    body = "\n".join(header) + "\n\n\n" + snippet.strip() + "\n"
    return body + _scratch(question, meta, uses_nodes)


def _drop_leading_comments(code: str) -> str:
    """LeetCode ships the node classes as a comment block on top; here they are real and come from leetkit."""
    lines = code.split("\n")
    while lines and (lines[0].startswith("#") or not lines[0].strip()):
        lines.pop(0)
    return "\n".join(lines)


def _fill_bodies(code: str) -> str:
    """Every method LeetCode left empty gets a body that says "not started" to the judge."""
    lines = [line.rstrip() for line in code.rstrip().split("\n")]
    out: list[str] = []
    for index, line in enumerate(lines):
        if not line and out and not out[-1]:
            continue
        out.append(line)
        if re.match(r"\s*def .*:$", line):
            indent = len(line) - len(line.lstrip())
            following = next((later for later in lines[index + 1:] if later.strip()), None)
            if following is None or len(following) - len(following.lstrip()) <= indent:
                out.append(" " * (indent + 4) + _STUB_BODY)
    while out and not out[-1]:
        out.pop()
    return "\n".join(out)


def _scratch(question: dict, meta: dict, uses_nodes: list) -> str:
    """A place to call your function by hand and print, for when you want to look before you test."""
    examples = question.get("exampleTestcaseList") or []
    if "classname" in meta or not examples or uses_nodes:
        return ""
    arguments = ", ".join(line.strip() for line in examples[0].split("\n"))
    arguments = arguments.replace("true", "True").replace("false", "False").replace("null", "None")
    return f'\n\nif __name__ == "__main__":\n    print(Solution().{meta.get("name", "solve")}({arguments}))\n'


_TEST_FILE = '''"""The cases live in cases.json, next to this file. Add your own there, or write extra tests below."""

from leetkit import problem_tests

test_case = problem_tests(__file__)
'''
