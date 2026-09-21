"""No test writes in the real journal or the real progress file."""

import pytest


@pytest.fixture(autouse=True)
def journal_file(tmp_path, monkeypatch):
    """No test writes in the real journal."""
    monkeypatch.setattr("leetkit.journal.PATH", tmp_path / "journal.jsonl")
    monkeypatch.setattr("leetkit.progress.PATH", tmp_path / "progress.json")          # nor in the real progress
    return tmp_path / "journal.jsonl"
