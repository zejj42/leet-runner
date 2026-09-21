# leet-runner

A local judge for LeetCode problems, driven from the command line. Python 3.10+, macOS or Linux.

## Install

    git clone https://github.com/zejj42/leet-runner.git
    cd leet-runner
    ./leet setup

`setup` creates `.venv` (no pip, nothing downloaded) and links `leet` into `~/.local/bin`. After it, `leet` runs
from any directory. If `~/.local/bin` is not on your `PATH` yet, log in again or add it.

## Usage

    leet code <problem>     edit the problem's solution.py in Neovim (vim if nvim is not installed)
    leet test <problem>     judge problems/<problem>/solution.py
    leet reset <problem>    restore solution.py to its empty stub (asks first; -y skips the question)
    leet open <problem>     open the statement and solution.py in VS Code (needs a desktop session)
    leet setup              create or repair .venv, the leet link and the VS Code extension
    leet update             git pull the newest problems and kit, then setup again; lists what changed
    leet --version          major.minor from pyproject.toml, then the commit count

`<problem>` is any of:

| Form | Example |
|---|---|
| LeetCode slug | `two-sum` |
| number on the list | `1` |
| words of the title | `two sum` |

Write the solution with `leet code`, or in any editor, then:

    $ leet code two-sum
    $ leet test two-sum
    Two Sum   Accepted   15 / 15 testcases passed   4 ms

    $ leet test two-sum
    Two Sum   Wrong Answer   1 / 15 testcases passed

      example 2
      Input       nums = [3, 2, 4]
                  target = 6
      Output      [0, 1]
      Expected    [1, 2]

Judging stops at the first failing case.

| Verdict | Meaning |
|---|---|
| `Accepted` | every case passed |
| `Wrong Answer` | the output differs from the expected one |
| `Runtime Error` | the solution raised; the exception and its line are shown |
| `Time Limit Exceeded` | a case ran longer than 2 s (10 s for a large case) |
| `Not started` | the method still raises `NotImplementedError` |

Exit codes: `0` Accepted or Not started, `1` any other verdict, `2` unknown problem or bad usage.

Every invocation is appended to `journal.jsonl` (git-ignored), one JSON object per line:

    {"at": "2026-09-21T17:30:59", "command": "test", "args": ["two-sum"], "exit": 0, "problem": "two-sum", "verdict": "Accepted", "passed": 15, "total": 15, "ms": 3}

## Problem folder

    problems/001_two_sum/
      README.md       statement
      solution.py     your code; not tracked by git, created from leetkit/stubs/
      cases.json      test cases
      large_*.json    data of cases too big to keep inline

## cases.json

    {
      "function": "twoSum",
      "params": [{"name": "nums", "type": "integer[]"}, {"name": "target", "type": "integer"}],
      "returns": "integer[]",
      "compare": "unordered",
      "cases": [
        {"name": "example 1", "args": [[2, 7, 11, 15], 9], "expected": [0, 1]}
      ]
    }

Add a case by adding a line to `cases`.

| Key | Values |
|---|---|
| `compare` | `exact` (default), `unordered`, `unordered_nested`, `float`, `any_of` (`expected` lists every right answer) |
| `time_limit` | seconds per case, default 2 |
| `returns: "void"` + `output_param: 0` | judge the argument the method changed in place |
| param type `ListNode`, `TreeNode` | built from LeetCode's notation: `[1, 2, 3]`, `[1, null, 2]` |
| param type `cycle position` | not passed to the method; links the tail of the preceding list to that index (`-1`: none) |
| case `"large": true` | five times the time limit |
| case `"file": "large_input.json"` | `args` and `expected` are read from that file |
| `"class": "LRUCache"` instead of `function` | design problems; cases carry `ops`, `args`, `expected` |

A `check.py` next to `cases.json` overrides `compare`: `check(args: dict, result, expected) -> bool | str`
(a string is the reason the answer is wrong).

## IDE support

VS Code, optional. The workspace recommends the Python and Code Runner extensions.

- ▶ on a `solution.py` judges it; the verdict appears, coloured, in the Output panel.
- F5 judges it under the debugger.
- ⇧⌘V previews a statement, styled by `.vscode/markdown.css`.

▶ works because `setup` writes a `.pth` file into `.venv`: when that Python runs a `solution.py` that has a
`cases.json` beside it, `leetkit/autorun.py` judges it on exit. Verdict colours come from
`vscode/verdict-colours`, a grammar-only extension that `setup` installs.

## Layout

    leet                 launcher (bash)
    problems.json        the problem list
    problems/            one folder per problem
    leetkit/
      cli.py             the leet commands
      judge.py           runs one case
      run.py             judges a folder, formats the verdict
      catalog.py         problem lookup
      structures.py      ListNode, TreeNode
      journal.py         journal.jsonl
      version.py         leet --version
      autorun.py         ▶ support
      colours.py         installs vscode/verdict-colours
      scaffold.py        builds a problem folder from LeetCode: python -m leetkit.scaffold <slug>
      statement.py       LeetCode HTML to Markdown
      stubs/             the empty solution.py of every problem, used by leet reset
    tests/               kit tests: python3 -m pytest (pytest is their only dependency)
