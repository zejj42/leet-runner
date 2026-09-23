"""The list of problems (problems.json, exported from LeetTracker) and where each one lives on disk."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent
PROBLEMS_DIR = ROOT / "problems"
STUBS_DIR = ROOT / "leetkit" / "stubs"          # each solution.py as it was before anyone wrote in it


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
    extra_id: Optional[int] = None        # an off-list problem that is not on LeetCode at all (x001)

    @property
    def label(self) -> str:
        if self.number is not None:
            return f"{self.number:03d}"
        return f"lc{self.leetcode_id:04d}" if self.leetcode_id is not None else f"x{self.extra_id:03d}"

    @property
    def folder(self) -> Path:
        return PROBLEMS_DIR / f"{self.label}_{self.slug.replace('-', '_')}"

    @property
    def stub(self) -> Path:
        return STUBS_DIR / f"{self.folder.name}.py"

    @property
    def url(self) -> str:
        return f"https://leetcode.com/problems/{self.slug}/" if self.leetcode_id is not None or self.number is not None else ""


def all_problems() -> list[Problem]:
    data = json.loads((ROOT / "problems.json").read_text())
    known = Problem.__dataclass_fields__                    # a newer problems.json may carry fields this code has not met
    return [Problem(**{k: v for k, v in entry.items() if k in known}) for entry in data["problems"]]


def find(reference: str) -> Problem:
    """By number on the list ("1"), off-list id ("lc904"), slug, folder name ("001_two_sum"), or words of the title."""
    problems = all_problems()
    text = reference.strip().lower()
    if text.isdigit():
        matches = [p for p in problems if p.number == int(text)]
    elif re.fullmatch(r"lc\d+", text):
        matches = [p for p in problems if p.leetcode_id == int(text[2:])]
    elif re.fullmatch(r"x\d+", text):
        matches = [p for p in problems if p.extra_id == int(text[1:])]
    else:
        slug = re.sub(r"^(\d{3}|lc\d{4}|x\d{3})_", "", text).replace("_", "-").replace(" ", "-")
        matches = [p for p in problems if p.slug == slug]
    if matches:
        return matches[0]

    words = text.replace("-", " ").replace("_", " ").split()
    matches = [p for p in problems if all(word in p.title.lower() for word in words)]
    if len(matches) == 1:
        return matches[0]
    if not matches:
        raise LookupError(f"No problem matches '{reference}'. Use its number on the list, or the slug from its LeetCode address, like two-sum.")
    raise LookupError(f"'{reference}' matches several: " + ", ".join(f"{p.label} {p.title}" for p in matches[:6]))
