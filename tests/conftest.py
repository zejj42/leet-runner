"""No test writes in the real journal or the real progress file."""

import pytest


@pytest.fixture(autouse=True)
def journal_file(tmp_path, monkeypatch):
    """No test writes in the real journal."""
    monkeypatch.setattr("leetkit.journal.PATH", tmp_path / "journal.jsonl")
    monkeypatch.setattr("leetkit.progress.PATH", tmp_path / "progress.json")          # nor in the real progress
    monkeypatch.setenv("LEET_TALLY", "cjk")                                          # whatever terminal runs the tests
    return tmp_path / "journal.jsonl"
