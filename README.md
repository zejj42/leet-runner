# leet-runner

The LeetTracker list (the 169 chart problems, then the off-list ones), to solve in VS Code and test locally.

## Setup, once

    ./leet setup

That also links the command into `~/.local/bin`, so from then on it is `leet`, from any folder.

Then open the folder in VS Code and accept the recommended Python extension.

## Day to day

Open a problem's `solution.py`, write your code, and press **▶ (Run Python File)** at the top right.
That judges the file against its cases and prints a verdict for each. F5 does the same with your breakpoints.
The Code Runner extension's ▶ works too: the workspace settings point it at this project's Python. `leet setup`
also installs a tiny extension (vscode/verdict-colours, a grammar and no code) that colours the verdict there.

    leet open two-sum    open its statement and solution in VS Code
    leet test two-sum    the same judging from the terminal
    leet reset two-sum   erase your code: solution.py goes back to its empty starting state (it asks first)

A problem is named by its LeetCode slug (`two-sum`, the end of its address), its number on the list (`1`),
or words from its title (`"two sum"`).

The Testing panel (the flask icon) also lists every case of every problem.

How ▶ works, since a `solution.py` holds nothing but your class: `leet setup` adds one line to the virtual
environment that notices when the file being run is a `solution.py` with a `cases.json` beside it, and judges it
once it has loaded. `leetkit/autorun.py` is all of it. Nothing else you run with this Python is affected.

## A problem's folder

    problems/001_two_sum/
      README.md          the statement, reworded; no follow-up, no hints
      solution.py        yours. Never overwritten by any command.
      cases.json         the test cases, one per line. Add your own. Never overwritten either.
      test_solution.py   turns cases.json into tests; extra tests of your own go below

Open a README's preview with ⇧⌘V: `.vscode/markdown.css` colours it, in light and dark.

A folder is made from LeetCode with `python -m leetkit.scaffold two-sum`; it never overwrites a solution, cases or a README.

A solution that still raises `NotImplementedError` counts as "not started": its tests are skipped, not failed.

## Adding cases

One line in `cases.json`:

    {"name": "what it checks", "args": [[1, 2, 3], 4], "expected": [0, 2]}

`"compare"` decides how an answer is judged: `exact`, `unordered` (any order), `unordered_nested`
(any order inside and out), `float`, or `any_of` (expected lists every right answer). Add `"stress": true`
to a large, slow case (the Testing panel leaves those out unless pytest gets `--stress`), and `"file": "big.json"` to keep large data out of the way.
Linked lists and trees are written LeetCode's way, `[1, 2, 3]` and `[1, null, 2]`. If a problem has many
right answers, a `check.py` beside it with `check(args, result, expected)` decides. `leetkit/judge.py` has the details.

## The kit

`leetkit/` is the judge, `ListNode` and `TreeNode`, and the scaffolder. `tests/` tests the kit itself.
`problems.json` is the list, exported from LeetTracker.
