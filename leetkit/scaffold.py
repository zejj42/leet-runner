"""Creates a problem's folder: the statement, a stub to write in, and the example cases.

Everything comes from LeetCode's public API. Nothing here ever writes a solution.
"""

from __future__ import annotations

import json
import re
import urllib.request
from pathlib import Path
from typing import Any, Optional

from .catalog import Problem
from .statement import example_outputs, to_markdown, without_follow_up

_QUERY = """query q($titleSlug: String!) { question(titleSlug: $titleSlug) {
  questionFrontendId title difficulty isPaidOnly content metaData exampleTestcaseList
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


def scaffold(problem: Problem) -> Path:
    """Writes what the folder does not have yet. What is there, written by hand, is never overwritten: a solution,
    cases, and the README, whose statement gets reworded so that it is this repo's own."""
    folder = problem.folder
    question = fetch(problem.slug)
    meta = json.loads(question.get("metaData") or "{}")
    folder.mkdir(parents=True, exist_ok=True)

    stub = _stub(problem, question, meta)
    problem.stub.parent.mkdir(parents=True, exist_ok=True)
    problem.stub.write_text(stub)                               # what `leet reset` puts back
    for name, content in (("README.md", _readme(problem, question)),
                          ("solution.py", stub),
                          ("cases.json", format_cases(_cases(question, meta)))):
        if content and not (folder / name).exists():
            (folder / name).write_text(content)
    return folder


# ---- README

def _readme(problem: Problem, question: dict) -> str:
    level = question["difficulty"].lower()
    where = " · ".join(part for part in (problem.topic, problem.list, problem.section) if part)
    lines = [f"# {question['questionFrontendId']}. {question['title']}", "",
             f'<span class="badge {level}">{question["difficulty"]}</span> <span class="where">{where}</span>', "",
             f"<{problem.url}>", ""]
    if question.get("isPaidOnly") or not question.get("content"):
        lines += ["This one is for LeetCode subscribers, so its statement could not be fetched. Paste it here.", ""]
    else:
        lines += [without_follow_up(to_markdown(question["content"])), ""]
    return "\n".join(lines)                                     # LeetCode's hints are left out too


# ---- cases.json

def _cases(question: dict, meta: dict) -> dict:
    params = [{"name": p["name"], "type": p["type"]} for p in meta.get("params", [])]
    snippet = next((s["code"] for s in question.get("codeSnippets") or [] if s["langSlug"] == "python3"), "")
    for before, param in zip(params, params[1:]):               # the cycle problems: pos shapes the list, and is not passed
        if param["name"] == "pos" and before["type"] == "ListNode" and not re.search(r"def \w+\([^)]*\bpos\b", snippet):
            param["type"] = "cycle position"
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

    header = [f'"""{question["questionFrontendId"]}. {question["title"]}  ({question["difficulty"]})', problem.url, "",
              "Press ▶ to judge this file.", '"""', ""]
    typing_names = [name for name in ("List", "Optional", "Dict", "Set", "Tuple") if re.search(rf"\b{name}\[", snippet)]
    if typing_names:
        header.append(f"from typing import {', '.join(typing_names)}")
    if uses_nodes:
        header.append(f"from leetkit import {', '.join(uses_nodes)}")
    while header and not header[-1]:
        header.pop()
    return "\n".join(header) + "\n\n\n" + snippet.strip() + "\n"


def _drop_leading_comments(code: str) -> str:
    """LeetCode ships the node classes as a comment block on top; here they are real and come from leetkit."""
    lines = code.split("\n")
    while lines and (lines[0].startswith("#") or not lines[0].strip()):
        lines.pop(0)
    return "\n".join(lines)


def _fill_bodies(code: str) -> str:
    """Every method LeetCode left empty gets a body that says "not started" to the judge. A body that is only
    LeetCode's note ("Do not return anything...") is empty too: the note stays, as the docstring it is."""
    lines = [line.rstrip() for line in code.rstrip().split("\n")]
    out: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        index += 1
        if not line and out and not out[-1]:
            continue
        out.append(line)
        if not re.match(r"\s*def .*:$", line):
            continue
        indent = len(line) - len(line.lstrip())
        body = []
        while index + len(body) < len(lines):
            later = lines[index + len(body)]
            if later.strip() and len(later) - len(later.lstrip()) <= indent:
                break
            body.append(later)
        text = "\n".join(body).strip()
        if text and not re.fullmatch(r'"""(?:(?!""").)*"""', text, flags=re.S):
            continue                                            # it has code of its own: leave it be
        out += [later for later in body if later.strip()] + [" " * (indent + 4) + _STUB_BODY, ""]
        index += len(body)
    while out and not out[-1]:
        out.pop()
    return "\n".join(out)


if __name__ == "__main__":                                  # python -m leetkit.scaffold two-sum
    import sys
    from .catalog import find
    print(scaffold(find(sys.argv[1])))
