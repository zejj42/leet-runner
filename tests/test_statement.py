"""LeetCode's HTML as Markdown, and Markdown laid out for a terminal."""

from leetkit.statement import example_outputs, to_markdown, without_follow_up


def test_statements_become_readable_markdown_without_the_follow_up():
    html = ("<p>Given <code>nums</code>, return <em>it</em>.</p><pre>\n<strong>Input:</strong> nums = [1]\n"
            "<strong>Output:</strong> [1]\n</pre><ul>\n\t<li><code>1 &lt;= n &lt;= 10<sup>4</sup></code></li></ul>"
            "<strong>Follow-up:&nbsp;</strong>Can you do better?")
    statement = without_follow_up(to_markdown(html))
    assert "Given `nums`, return *it*." in statement
    assert "> **Input:** `nums = [1]`" in statement and "> **Output:** `[1]`" in statement      # an example, as a quote
    assert "```" not in statement
    assert "`1 <= n <= 10^4`" in statement
    assert "Follow" not in statement and "do better" not in statement
    assert example_outputs(html) == ["[1]"]


def test_a_block_that_is_not_an_example_stays_a_code_block():
    assert "```\n  1\n / \\\n2   3\n```" in to_markdown("<pre>\n  1\n / \\\n2   3\n</pre>")


def test_the_newer_example_markup_reads_like_the_older_one():
    html = ('<p><strong class="example">Example 1:</strong></p>\n<div class="example-block">\n'
            '<p><strong>Input:</strong> <span class="example-io">head = [1,2]</span></p>\n'
            '<p><strong>Output:</strong> <span class="example-io">[2,1]</span></p>\n<p><strong>Explanation:</strong></p>\n'
            '<p><img alt="" src="https://x/y.jpg" /></p>\n</div>\n<p><strong>Constraints:</strong></p>')
    text = to_markdown(html)
    assert "> **Input:** `head = [1,2]`" in text and "> **Output:** `[2,1]`" in text
    assert "Explanation" not in text and "![](https://x/y.jpg)" in text and "**Constraints:**" in text
    assert without_follow_up("the end.** Follow up:** Do better?") == "the end."


def test_bold_words_in_one_sentence_keep_to_themselves():
    text = to_markdown("<p><strong>Note:</strong> You are <strong>not</strong> allowed.</p>\n<p>&nbsp;</p>\n<p><strong class=\"example\">Example 1:</strong></p>")
    assert "**Note:** You are **not** allowed." in text and "\n**Example 1:**" in text
    assert "**Output:** x" in to_markdown("<p><strong>Output: </strong>x</p>")


def test_emphasis_that_ends_in_a_space_and_runs_into_more_emphasis_stays_well_formed():
    text = to_markdown("<p>return <em>the length of the longest </em><strong><em>substring</em></strong>.</p>")
    assert "return *the length of the longest* ***substring***." in text


def test_a_statement_is_laid_out_for_the_terminal():
    from leetkit.reader import render
    text = render("# 1. Two Sum\n\n<span class=\"badge easy\">Easy</span> <span class=\"where\">array · First 75</span>\n\n"
                  "<https://leetcode.com/problems/two-sum/>\n\nYou get `nums` and **exactly** one *pair* of them " + "adds up " * 20 + "\n\n"
                  "**Example 1:**\n\n![](https://x/y.png)\n\n> **Input:** `nums = [2,7]`  \n> **Output:** `[0,1]`  \n\n"
                  "```\nL0 → L1\n```\n\n**Constraints:**\n\n - `2 <= nums.length <= 10^4`\n", colour=False, width=60)
    assert text.startswith("1. Two Sum\n\nEasy   array · First 75\n\nhttps://leetcode.com/problems/two-sum/\n")
    assert "You get nums and exactly one pair of them" in text and max(len(row) for row in text.split("\n")) <= 60
    assert "Example 1:\n" in text and "(picture)  https://x/y.png" in text
    assert "  │ Input: nums = [2,7]\n  │ Output: [0,1]" in text
    assert "    L0 → L1" in text and "  • 2 <= nums.length <= 10^4" in text
    assert "*" not in text and "`" not in text and "<" not in text.replace("<=", "")
    assert "\033[1;32mEasy" in render('<span class="badge easy">Easy</span>', colour=True)
