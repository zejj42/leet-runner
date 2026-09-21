"""A problem's README.md, laid out for a terminal: leet read two-sum.

Only what the statements in this repo use is understood: a heading, the difficulty badge, bold, italic, `code`,
quoted examples, lists, fenced blocks, links and pictures. Colours are left out when the output is not a terminal.
"""

from __future__ import annotations

import re
import shutil

_ANSI = re.compile(r"\033\[[0-9;]*m")
_LEVELS = {"easy": "1;32", "medium": "1;33", "hard": "1;31"}


def render(markdown: str, colour: bool = True, width: int | None = None) -> str:
    width = width or min(shutil.get_terminal_size((88, 24)).columns, 96)

    def paint(text: str, code: str) -> str:
        return f"\033[{code}m{text}\033[0m" if colour else text

    def inline(text: str) -> str:
        text = re.sub(r"`([^`]+)`", lambda m: paint(m.group(1), "36"), text)
        text = re.sub(r"\*\*\*(.+?)\*\*\*", lambda m: paint(m.group(1), "1;3"), text)
        text = re.sub(r"\*\*(.+?)\*\*", lambda m: paint(m.group(1), "1"), text)
        return re.sub(r"(?<![\w*])\*([^*\n]+?)\*(?![\w*])", lambda m: paint(m.group(1), "3"), text)

    out: list[str] = []
    fenced = False
    for line in markdown.split("\n"):
        line = line.rstrip()
        if line.strip() == "```":
            fenced = not fenced
            continue
        if fenced:
            out.append("    " + paint(line, "36"))
        elif line.startswith("# "):
            out.append(paint(line[2:], "1"))
        elif "<span" in line:                                   # the badge line: difficulty, then where it sits
            level = re.search(r'class="badge (\w+)">([^<]+)<', line)
            where = re.search(r'class="where">([^<]+)<', line)
            out.append("   ".join(part for part in (paint(level.group(2), _LEVELS.get(level.group(1), "1")) if level else "",
                                                    paint(where.group(1), "2") if where else "") if part))
        elif re.fullmatch(r"<https?://[^>]+>", line):
            out.append(paint(line[1:-1], "2"))
        elif re.fullmatch(r"!\[[^\]]*\]\([^)]+\)", line):
            out.append(paint("(picture)  " + re.search(r"\(([^)]+)\)", line).group(1), "2"))
        elif re.fullmatch(r"\*\*(Example \d+|Constraints):\*\*", line):
            out.append(paint(line.strip("*"), "1;33"))
        elif line.startswith(">"):
            out += [paint("  │ ", "32") + row for row in _wrap(inline(line[1:].strip()), width - 4)]
        elif re.match(r"\s*- ", line):
            rows = _wrap(inline(line.strip()[2:]), width - 4)
            out += ["  • " + rows[0]] + ["    " + row for row in rows[1:]]
        else:
            out += _wrap(inline(line), width) if line else [""]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip("\n") + "\n"


def _wrap(text: str, width: int) -> list[str]:
    """Breaks at spaces, counting only what shows: colour codes take no room."""
    rows, row, room = [], [], width
    for word in text.split(" "):
        size = len(_ANSI.sub("", word))
        if row and size + 1 > room:
            rows.append(" ".join(row))
            row, room = [], width
        row.append(word)
        room -= size + 1
    return rows + [" ".join(row)] if row or not rows else rows
