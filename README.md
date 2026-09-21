# leet-practice

The LeetTracker list (the 169 chart problems, then the off-list ones), to solve in VS Code and test locally.

## Setup, once

    python3 -m venv .venv && .venv/bin/pip install -r requirements.txt

Open the folder in VS Code and accept the recommended Python extension.

## Day to day

    ./leet next            the first problem on the list you have not passed
    ./leet new 2           create problem 2's folder from LeetCode (number, lc904, slug, or part of the title)
    ./leet test 2          run its tests        add --stress for the large cases
    ./leet test            run everything you have started
    ./leet list            how each problem stands        --all for the whole list
    ./leet open 2          open its statement and solution in VS Code

In VS Code: write in `solution.py`, then **Terminal > Run Test Task** (or ⇧⌘P "Run Test Task") tests the
problem whose file is open. The Testing panel lists every case. F5 with "Debug this problem's tests" stops
at your breakpoints; "Run this file" runs the little `__main__` block at the bottom of a solution.

## A problem's folder

    problems/001_two_sum/
      README.md          the statement; the follow-up and LeetCode's hints are folded shut
      solution.py        yours. Never overwritten by any command.
      cases.json         the test cases, one per line. Add your own.
      test_solution.py   turns cases.json into tests; extra tests of your own go below

A solution that still raises `NotImplementedError` counts as "not started": its tests are skipped, not failed.

## Adding cases

One line in `cases.json`:

    {"name": "what it checks", "args": [[1, 2, 3], 4], "expected": [0, 2]}

`"compare"` decides how an answer is judged: `exact`, `unordered` (any order), `unordered_nested`
(any order inside and out), `float`, or `any_of` (expected lists every right answer). Add `"stress": true`
to a case that should only run with `--stress`, and `"file": "big.json"` to keep large data out of the way.
Linked lists and trees are written LeetCode's way, `[1, 2, 3]` and `[1, null, 2]`. If a problem has many
right answers, a `check.py` beside it with `check(args, result, expected)` decides. `leetkit/judge.py` has the details.

## The kit

`leetkit/` is the judge, `ListNode` and `TreeNode`, and the scaffolder. `tests/` tests the kit itself.
`problems.json` is the list, exported from LeetTracker.
