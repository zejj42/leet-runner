"""Turns the HTML of a LeetCode problem statement into Markdown for the problem's README."""

from __future__ import annotations

import re
from html.parser import HTMLParser


class _Markdown(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []
        self.in_pre = False
        self.lists: list[list] = []          # a stack of [kind, counter]

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "pre":
            self.in_pre = True
            self.out.append("\n```\n")
        elif self.in_pre:
            return
        elif tag in ("strong", "b"):
            self.out.append("**")
        elif tag in ("em", "i"):
            self.out.append("*")
        elif tag == "code":
            self.out.append("`")
        elif tag == "sup":
            self.out.append("^")
        elif tag == "sub":
            self.out.append("_")
        elif tag in ("ul", "ol"):
            self.lists.append([tag, 0])
            self.out.append("\n")
        elif tag == "li":
            kind, count = self.lists[-1] if self.lists else ("ul", 0)
            if self.lists:
                self.lists[-1][1] = count + 1
            indent = "  " * max(len(self.lists) - 1, 0)
            self.out.append(f"{indent}{count + 1}. " if kind == "ol" else f"{indent}- ")
        elif tag == "img" and attrs.get("src"):
            self.out.append(f"\n![{attrs.get('alt', '')}]({attrs['src']})\n")
        elif tag == "br":
            self.out.append("\n")

    def handle_endtag(self, tag):
        if tag == "pre":
            self.in_pre = False
            self.out.append("\n```\n")
        elif self.in_pre:
            return
        elif tag in ("strong", "b"):
            self.out.append("**")
        elif tag in ("em", "i"):
            self.out.append("*")
        elif tag == "code":
            self.out.append("`")
        elif tag in ("p", "div"):
            self.out.append("\n\n")
        elif tag == "li":
            self.out.append("\n")
        elif tag in ("ul", "ol"):
            if self.lists:
                self.lists.pop()
            self.out.append("\n")

    def handle_data(self, data):
        self.out.append(data if self.in_pre else data.replace("\n", " "))


def to_markdown(html: str) -> str:
    parser = _Markdown()
    parser.feed(html or "")
    text = "".join(parser.out).replace("\xa0", " ")
    text = re.sub(r"\*\*([^*\n]+?)\s+\*\*", r"**\1** ", text)      # "**Output: **x" renders as literal stars
    text = re.sub(r"\*\*\*\*", "", text)

    # Outside code fences, lines start at the margin (list items keep their nesting); inside, nothing is touched
    # except the blank lines LeetCode leaves at the top and bottom of every example.
    lines, fenced = [], False
    for line in text.split("\n"):
        if line.strip() == "```":
            if fenced:
                while lines and not lines[-1].strip():
                    lines.pop()
            fenced = not fenced
            lines.append("```")
            if not fenced:
                lines.append("")
        elif fenced:
            if line.strip() or lines[-1] != "```":
                lines.append(line.rstrip())
        else:
            stripped = line.strip()
            nested = re.match(r"(\s*)(- |\d+\. )", line.replace("\t", ""))
            lines.append((nested.group(1) if nested and stripped else "") + re.sub(r"\s+", " ", stripped))
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def split_follow_up(markdown: str) -> tuple[str, str]:
    """The statement, and its "Follow-up" separately: that part names the target, so the README folds it away."""
    match = re.search(r"\*\*Follow[- ]?up:?\s*\*\*:?", markdown, flags=re.IGNORECASE)
    if not match:
        return markdown, ""
    return markdown[:match.start()].strip(), markdown[match.end():].strip()


def example_outputs(html: str) -> list[str]:
    """The text after each "Output:" in the statement's examples, in order."""
    found = re.findall(r"<strong[^>]*>\s*Output:?\s*</strong>:?\s*(.*?)(?=<strong|</pre>|</p>|\n)", html or "", flags=re.S)
    return [re.sub(r"<[^>]+>", "", item).replace("&quot;", '"').replace("\xa0", " ").strip() for item in found]
