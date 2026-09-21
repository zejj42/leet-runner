"""The leet commands."""

import json
import os
import subprocess

import pytest

from leetkit import scaffold as scaffolding
from leetkit.catalog import all_problems, find

from helpers import _git, ADD, problem, QUESTION


def test_the_command_takes_a_number_a_slug_or_title_words_and_nothing_else(capsys):
    from leetkit import cli
    for words in (["1"], ["two-sum"], ["Two", "Sum"], ["001_two_sum"]):
        assert cli._in_the_repo(words).slug == "two-sum"
    assert cli.main(["test", "no-such-problem-at-all"]) == 2 and "No problem matches" in capsys.readouterr().err
    assert cli.main(["test", "valid-parentheses"]) in (0, 1, 2)            # on the list; judged once its folder exists
    for gone in (["new", "2"], ["next"], ["test"], ["open"]):
        with pytest.raises(SystemExit):
            cli.main(gone)


def test_every_command_is_journalled_whatever_came_of_it(journal_file, tmp_path, monkeypatch):
    from leetkit import cli
    (tmp_path / "add").mkdir()
    folder = problem(tmp_path / "add", "class Solution:\n    def add(self, a, b): return a - b", ADD)
    real = cli._in_the_repo
    added = type("P", (), {"slug": "add", "folder": folder, "title": "Add"})()
    monkeypatch.setattr(cli, "_in_the_repo", lambda words: added if words == ["add"] else real(words))
    assert cli.main(["test", "add"]) == 1
    assert cli.main(["test", "no-such-problem-at-all"]) == 2
    with pytest.raises(SystemExit):
        cli.main(["next"])

    lines = [json.loads(line) for line in journal_file.read_text().splitlines()]
    assert [(line["command"], line["args"], line["exit"]) for line in lines] == [
        ("test", ["add"], 1), ("test", ["no-such-problem-at-all"], 2), ("next", [], 2)]
    assert lines[0]["verdict"] == "Wrong Answer" and (lines[0]["passed"], lines[0]["total"]) == (0, 1)
    assert lines[0]["problem"] == "add" and lines[0]["failed_case"] == "small" and "at" in lines[0]
    assert "No problem matches" in lines[1]["error"]


def test_list_names_every_problem_in_the_repo_and_pages_only_a_tall_list_on_a_terminal(monkeypatch, capsys):
    from leetkit import cli
    assert cli.main(["list"]) == 0
    said = capsys.readouterr().out
    assert "  001  Two Sum" in said and "0 of " in said and "two-sum" in said and "142  Reorder List" in said and "medium" in said
    assert said.index("001") < said.index("003") < said.index("142") and "solved.  leet read" in said

    paged = []
    monkeypatch.setattr(cli.sys.stdout, "isatty", lambda: True, raising=False)
    monkeypatch.setattr(cli.shutil, "get_terminal_size", lambda fallback: os.terminal_size((80, 5)))
    monkeypatch.setattr(cli.shutil, "which", lambda name: "/usr/bin/less")
    monkeypatch.setattr(cli.subprocess, "run", lambda command, input, text: paged.append(command))
    cli._show("\n".join(str(n) for n in range(3)))               # fits: printed
    assert paged == [] and "0\n1\n2" in capsys.readouterr().out
    cli._show("\n".join(str(n) for n in range(30)))              # too tall: through less
    assert paged == [["less", "-FRX"]]


def test_every_statement_in_the_repo_can_be_read(capsys):
    from leetkit import cli
    from leetkit.catalog import all_problems
    for problem in all_problems():
        if problem.folder.exists():
            assert cli.main(["read", problem.slug]) == 0
            said = capsys.readouterr().out
            assert problem.title in said and "**" not in said and "<span" not in said, problem.title


@pytest.mark.parametrize("installed, chosen", [({"nvim", "vim"}, "nvim"), ({"vim"}, "vim"), ({"nvim"}, "nvim")])
def test_leet_code_opens_the_solution_in_neovim_or_else_vim_from_inside_its_folder(monkeypatch, journal_file, installed, chosen):
    from leetkit import cli
    started = {}
    monkeypatch.setattr(cli.shutil, "which", lambda name: f"/usr/bin/{name}" if name in installed else None)
    monkeypatch.setattr(cli.subprocess, "call", lambda command, cwd: started.update(command=command, cwd=cwd) or 0)
    assert cli.main(["code", "two", "sum"]) == 0
    assert started == {"command": [chosen, "solution.py"], "cwd": find("two-sum").folder}
    entry = json.loads(journal_file.read_text())
    assert (entry["problem"], entry["editor"]) == ("two-sum", chosen)


def test_leet_code_says_so_when_there_is_no_editor(monkeypatch, capsys):
    from leetkit import cli
    monkeypatch.setattr(cli.shutil, "which", lambda name: None)
    assert cli.main(["code", "two-sum"]) == 2 and "Neither nvim nor vim" in capsys.readouterr().err


def test_open_says_why_when_vs_code_cannot_open_a_window(monkeypatch, capsys):
    from leetkit import cli
    monkeypatch.setattr(cli.subprocess, "call", lambda command: 0)
    monkeypatch.setattr(cli.shutil, "which", lambda name: "/usr/bin/code")
    monkeypatch.setenv("SSH_CONNECTION", "10.0.0.6 1 10.0.0.12 22")
    monkeypatch.delenv("TERM_PROGRAM", raising=False)
    assert cli.main(["open", "two-sum"]) == 1 and "ssh session" in capsys.readouterr().out
    monkeypatch.setenv("TERM_PROGRAM", "vscode")                  # VS Code's own remote terminal can
    assert cli.main(["open", "two-sum"]) == 0
    monkeypatch.delenv("SSH_CONNECTION")
    monkeypatch.setattr(cli.shutil, "which", lambda name: None)
    assert cli.main(["open", "two-sum"]) == 1 and "leet code two-sum" in capsys.readouterr().out


def test_a_problem_without_a_solution_file_gets_its_empty_stub(tmp_path, monkeypatch):
    from leetkit import cli
    monkeypatch.setattr("leetkit.catalog.PROBLEMS_DIR", tmp_path)
    two_sum = find("two-sum")
    two_sum.folder.mkdir()
    assert cli._in_the_repo(["two-sum"]).slug == "two-sum"
    assert (two_sum.folder / "solution.py").read_text() == two_sum.stub.read_text()
    (two_sum.folder / "solution.py").write_text("mine")
    cli.lay_out_solutions()
    assert (two_sum.folder / "solution.py").read_text() == "mine"


def test_reset_puts_the_empty_solution_back_but_only_after_a_yes(tmp_path, monkeypatch, capsys):
    from leetkit import cli
    monkeypatch.setattr(scaffolding, "fetch", lambda slug: QUESTION)
    monkeypatch.setattr("leetkit.catalog.PROBLEMS_DIR", tmp_path)
    monkeypatch.setattr("leetkit.catalog.STUBS_DIR", tmp_path / "stubs")
    monkeypatch.setattr("leetkit.cli.ROOT", tmp_path)
    solution = scaffolding.scaffold(find("two-sum")) / "solution.py"
    empty = solution.read_text()

    assert cli.main(["reset", "two-sum"]) == 0 and "already" in capsys.readouterr().out   # nothing to erase, nothing asked

    solution.write_text("my code")
    monkeypatch.setattr("builtins.input", lambda prompt: "")
    assert cli.main(["reset", "two-sum"]) == 1 and solution.read_text() == "my code"      # Enter alone means no
    monkeypatch.setattr("builtins.input", lambda prompt: "y")
    assert cli.main(["reset", "two-sum"]) == 0 and solution.read_text() == empty

    solution.write_text("my code")
    monkeypatch.setattr("builtins.input", lambda prompt: pytest.fail("asked, despite --yes"))
    assert cli.main(["reset", "1", "--yes"]) == 0 and solution.read_text() == empty


def test_every_problem_in_the_repo_can_be_reset():
    from leetkit.catalog import all_problems
    for problem in all_problems():
        if problem.folder.exists():
            assert "raise NotImplementedError" in problem.stub.read_text(), problem.title


def test_startover_empties_every_solution_and_forgets_what_was_solved_after_a_yes(tmp_path, monkeypatch, capsys):
    from leetkit import cli, progress
    monkeypatch.setattr("leetkit.catalog.PROBLEMS_DIR", tmp_path)
    written, untouched = find("two-sum"), find("reorder-list")
    for one in (written, untouched):
        one.folder.mkdir()
        (one.folder / "solution.py").write_text(one.stub.read_text())
    (written.folder / "solution.py").write_text("my code")
    (written.folder / "cases.json").write_text("my cases")
    progress.mark_solved("two-sum")

    monkeypatch.setattr("builtins.input", lambda prompt: "")
    assert cli.main(["startover"]) == 1                                     # Enter alone means no
    assert "1 problem" in capsys.readouterr().out and (written.folder / "solution.py").read_text() == "my code"
    assert list(progress.solved()) == ["two-sum"]

    monkeypatch.setattr("builtins.input", lambda prompt: "y")
    assert cli.main(["startover"]) == 0
    assert (written.folder / "solution.py").read_text() == written.stub.read_text()
    assert (written.folder / "cases.json").read_text() == "my cases" and progress.solved() == {}

    monkeypatch.setattr("builtins.input", lambda prompt: pytest.fail("nothing to erase, nothing to ask"))
    assert cli.main(["startover"]) == 0 and "Nothing to start over" in capsys.readouterr().out


def test_update_brings_new_problems_and_leaves_what_you_wrote_alone(tmp_path, monkeypatch, capsys):
    from leetkit import cli
    origin, clone = tmp_path / "origin", tmp_path / "clone"
    (origin / "problems" / "001_two_sum").mkdir(parents=True)
    (origin / ".gitignore").write_text("problems/*/solution.py\n")
    (origin / "problems" / "001_two_sum" / "cases.json").write_text('{\n  "cases": [\n    1\n  ]\n}\n')
    _git(origin, "init", "-q", "-b", "main"); _git(origin, "add", "-A"); _git(origin, "commit", "-qm", "one")
    subprocess.run(["git", "clone", "-q", str(origin), str(clone)], check=True)

    (clone / "problems" / "001_two_sum" / "solution.py").write_text("my code")                       # not in git at all
    (clone / "problems" / "001_two_sum" / "cases.json").write_text('{\n  "cases": [\n    1,\n    "mine"\n  ]\n}\n')
    (origin / "problems" / "003_merge_two_sorted_lists").mkdir()
    (origin / "problems" / "003_merge_two_sorted_lists" / "cases.json").write_text("{}")
    _git(origin, "add", "-A"); _git(origin, "commit", "-qm", "two")

    monkeypatch.setattr(cli, "ROOT", clone)
    monkeypatch.setattr("leetkit.catalog.PROBLEMS_DIR", clone / "problems")
    again = []
    monkeypatch.setattr(cli, "_setup_again", lambda: again.append(True) or 0)
    assert cli.main(["update"]) == 0
    said = capsys.readouterr().out
    assert "Updated  0.0.1 → 0.0.2" in said and "· two" in said and "· Merge Two Sorted Lists     leet read merge-two-sorted-lists" in said and again == [True]
    assert (clone / "problems" / "003_merge_two_sorted_lists" / "cases.json").exists()
    assert (clone / "problems" / "001_two_sum" / "solution.py").read_text() == "my code"
    assert '"mine"' in (clone / "problems" / "001_two_sum" / "cases.json").read_text()

    assert cli.main(["update"]) == 0 and "Already up to date" in capsys.readouterr().out and again == [True]


def test_the_colour_extension_packs_into_something_vs_code_can_install(tmp_path):
    import zipfile
    from leetkit.colours import pack
    names = zipfile.ZipFile(pack(tmp_path / "colours.vsix")).namelist()
    assert {"[Content_Types].xml", "extension.vsixmanifest", "extension/package.json",
            "extension/syntaxes/verdict.tmLanguage.json"} <= set(names)
