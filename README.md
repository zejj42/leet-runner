# leet-practice

The LeetTracker list (the 169 chart problems, then the off-list ones), to solve in VS Code and test locally.

## Setup, once

    ./leet setup

Then open the folder in VS Code and accept the recommended Python extension.

## Day to day

Open a problem's `solution.py`, write your code, and press **▶ (Run Python File)** at the top right.
That judges the file against its cases and prints a verdict for each. F5 does the same with your breakpoints.

    ./leet next            the first problem on the list you have not passed
    ./leet new 2           create problem 2's folder from LeetCode (number, lc904, slug, or part of the title)
    ./leet list            how each problem stands        --all for the whole list
    ./leet open 2          open its statement and solution in VS Code
    ./leet test 2 --stress the same judging from the terminal, here with the large cases too
    ./leet test            everything you have started

The Testing panel (the flask icon) also lists every case of every problem.

How ▶ works, since a `solution.py` holds nothing but your class: `./leet setup` adds one line to the virtual
environment that notices when the file being run is a `solution.py` with a `cases.json` beside it, and judges it
once it has loaded. `leetkit/autorun.py` is all of it. Nothing else you run with this Python is affected.

## A problem's folder

    problems/001_two_sum/
      README.md          the statement; the follow-up and LeetCode's hints are folded shut
      solution.py        yours. Never overwritten by any command.
      cases.json         the test cases, one per line. Add your own. Never overwritten either.
      scratch.py         call your solution by hand and print; F5 > "Run this file"
      test_solution.py   turns cases.json into tests; extra tests of your own go below

Open a README's preview with ⇧⌘V: `.vscode/markdown.css` colours it, in light and dark.
`./leet new 2 --force` refreshes a problem's README and test file and nothing else.

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
