# leet-runner

The LeetTracker list (the 169 chart problems, then the off-list ones), to solve in VS Code and judge locally.

## Setup, once

    ./leet setup

It creates `.venv`, links the command into `~/.local/bin` (from then on it is `leet`, from any folder), and
installs the small VS Code extension that colours verdicts. Then open the folder in VS Code and accept the
recommended extensions: Python, and Code Runner for its ▶.

## Day to day

Open a problem's `solution.py`, write your code, and press **▶**. The verdict shows in the Output panel:

    Two Sum   Accepted   15 / 15 testcases passed   4 ms

When it is not Accepted, the first case that went wrong follows, with its input, your output and what was
expected. F5 judges the same file, stopping at your breakpoints.

    leet open two-sum    open its statement and solution in VS Code
    leet test two-sum    the same judging, from the terminal
    leet reset two-sum   erase your code: solution.py goes back to its empty starting state (it asks first)

A problem is named by its LeetCode slug (`two-sum`, the end of its address), its number on the list (`1`),
or words from its title (`two sum`). Every `leet` command is written to `journal.jsonl`, one line each,
with the verdict when it was a test.

## A problem's folder

    problems/001_two_sum/
      README.md          the statement, in this repo's words; no follow-up, no hints. ⇧⌘V previews it, in colour.
      solution.py        yours
      cases.json         the test cases, one per line. Add your own.
      large_*.json       the data of a case too big to read

A solution that still raises `NotImplementedError` is "Not started", not wrong.

## Adding cases

One line in `cases.json`:

    {"name": "what it checks", "args": [[1, 2, 3], 4], "expected": [0, 2]}

`"compare"` decides how an answer is judged: `exact`, `unordered` (any order), `unordered_nested`
(any order inside and out), `float`, or `any_of` (expected lists every right answer). `"large": true` gives
a case five times the time limit, and `"file": "large_input.json"` keeps its data out of the way.
Linked lists and trees are written LeetCode's way, `[1, 2, 3]` and `[1, null, 2]`. If a problem has many
right answers, a `check.py` beside it with `check(args, result, expected)` decides. `leetkit/judge.py` has the details.

## The kit

    leet                 the command: a few lines of bash that start leetkit with the project's Python
    problems.json        the list, exported from LeetTracker
    leetkit/
      cli.py             leet test, open, reset, setup
      judge.py           runs one case: builds the arguments, calls your method, compares
      run.py             judges a folder and words the verdict
      autorun.py         what makes ▶ on a solution.py judge it
      structures.py      ListNode, TreeNode, and LeetCode's list notation for them
      catalog.py         finds a problem by number, slug or title
      journal.py         journal.jsonl
      scaffold.py        makes a problem's folder from LeetCode: python -m leetkit.scaffold two-sum
      statement.py       LeetCode's HTML statement as Markdown
      colours.py         packs and installs vscode/verdict-colours
      stubs/             every solution.py as it started, for leet reset
    tests/               the kit's own tests: .venv/bin/python -m pytest

How ▶ works, since a `solution.py` holds nothing but your class: `leet setup` adds one line to the virtual
environment that notices when the file being run is a `solution.py` with a `cases.json` beside it, and judges
it once it has loaded. Nothing else you run with this Python is affected.
