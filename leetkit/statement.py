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


def _example_blocks_as_pre(html: str) -> str:
    """LeetCode's newer examples are a <div class="example-block"> of paragraphs. Rewritten as the older <pre> of
    "Label: value" lines, they take the same road as every other example. A picture inside comes out after it."""
    def convert(match: re.Match) -> str:
        inner = match.group(1)
        pictures = re.findall(r"<img[^>]*>", inner)
        rows = []
        for paragraph in re.findall(r"<p>(.*?)</p>", re.sub(r"<img[^>]*>", "", inner), flags=re.S):
            label = re.match(r"\s*<strong>([^<]*)</strong>\s*(.*)", paragraph, flags=re.S)
            text = re.sub(r"<[^>]+>", "", label.group(2) if label else paragraph).strip()
            if label and text:
                rows.append(f"<strong>{label.group(1)}</strong> {text}")
            elif text:
                rows.append(text)
        return "<pre>\n" + "\n".join(rows) + "\n</pre>\n" + "".join(f"<p>{picture}</p>\n" for picture in pictures)
    return re.sub(r'<div class="example-block">(.*?)</div>', convert, html, flags=re.S)


def to_markdown(html: str) -> str:
    parser = _Markdown()
    parser.feed(_example_blocks_as_pre(html or ""))
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
    text = _examples_as_blocks("\n".join(lines))
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


_LABEL = re.compile(r"^(Input|Output|Explanation|Note):\s*(.*)$")


def _examples_as_blocks(text: str) -> str:
    """LeetCode's examples come as a grey block of "Input: / Output: / Explanation:" lines. As a quote with bold
    labels and the values as code they can be styled (see .vscode/markdown.css) and read better even unstyled.
    Any other fenced block (a drawing, a table) is left exactly as it is."""
    def convert(match: re.Match) -> str:
        rows = [row for row in match.group(1).split("\n") if row.strip()]
        if not rows or not _LABEL.match(rows[0]):
            return match.group(0)
        out: list[str] = []
        for row in rows:
            labelled = _LABEL.match(row)
            if labelled and labelled.group(1) in ("Input", "Output"):
                out.append(f"> **{labelled.group(1)}:** `{labelled.group(2)}`  ")
            elif labelled:
                out.append(f"> **{labelled.group(1)}:** {labelled.group(2)}  ")
            else:
                out.append(f"> {row.strip()}  ")                     # an explanation that runs on
        return "\n".join(out) + "\n"
    return re.sub(r"```\n(.*?)\n```\n", convert, text, flags=re.S)


def without_follow_up(markdown: str) -> str:
    """The statement up to its "Follow-up": that part names the target to aim for, which is a hint."""
    match = re.search(r"\*\*\s*Follow[- ]?up:?\s*\*\*:?", markdown, flags=re.IGNORECASE)
    return markdown[:match.start()].strip() if match else markdown


def example_outputs(html: str) -> list[str]:
    """The text after each "Output:" in the statement's examples, in order."""
    found = re.findall(r"<strong[^>]*>\s*Output:?\s*</strong>:?\s*(.*?)(?=<strong|</pre>|</p>|\n)", html or "", flags=re.S)
    return [re.sub(r"<[^>]+>", "", item).replace("&quot;", '"').replace("\xa0", " ").strip() for item in found]
