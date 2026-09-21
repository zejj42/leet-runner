"""The list of problems (problems.json, exported from LeetTracker) and where each one lives on disk."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent
PROBLEMS_DIR = ROOT / "problems"


@dataclass(frozen=True)
class Problem:
    title: str
    slug: str
    difficulty: str
    topic: str
    list: str
    section: str
    number: Optional[int] = None          # its place on the chart, 1...169
    leetcode_id: Optional[int] = None     # only known for off-list problems

    @property
    def label(self) -> str:
        return f"{self.number:03d}" if self.number is not None else f"lc{self.leetcode_id:04d}"

    @property
    def folder(self) -> Path:
        return PROBLEMS_DIR / f"{self.label}_{self.slug.replace('-', '_')}"

    @property
    def url(self) -> str:
        return f"https://leetcode.com/problems/{self.slug}/"


def all_problems() -> list[Problem]:
    data = json.loads((ROOT / "problems.json").read_text())
    return [Problem(**entry) for entry in data["problems"]]


def find(reference: str) -> Problem:
    """By chart number ("1", "001"), off-list id ("lc904"), slug, folder path, or any part of the title."""
    problems = all_problems()
    text = reference.strip().rstrip("/")
    name = Path(text).name.lower()                       # accepts problems/001_two_sum or a file inside it
    if Path(text).suffix:
        name = Path(text).parent.name.lower()

    for candidate in {text.lower(), name}:
        if candidate.isdigit():
            matches = [p for p in problems if p.number == int(candidate)]
        elif re.fullmatch(r"lc\d+", candidate):
            matches = [p for p in problems if p.leetcode_id == int(candidate[2:])]
        else:
            prefix = re.match(r"(\d{3}|lc\d{4})_", candidate)
            slug = candidate[prefix.end():] if prefix else candidate
            slug = slug.replace("_", "-").replace(" ", "-")
            matches = [p for p in problems if p.slug == slug]
        if matches:
            return matches[0]

    words = text.lower().replace("-", " ").split()
    matches = [p for p in problems if all(word in p.title.lower() for word in words)]
    if len(matches) == 1:
        return matches[0]
    if not matches:
        raise LookupError(f"No problem matches '{reference}'. Try ./leet list --all")
    raise LookupError(f"'{reference}' matches several: " + ", ".join(f"{p.label} {p.title}" for p in matches[:6]))
