"""The two node types LeetCode hands you, and the conversions between them and plain lists.

LeetCode writes a linked list as [1, 2, 3] and a binary tree level by level with null for a missing
child, e.g. [1, null, 2, 3]. The judge uses these functions to build the arguments for your solution
and to turn what it returns back into a list that can be compared and printed.
"""

from __future__ import annotations

from collections import deque
from typing import Any, Optional


class ListNode:
    def __init__(self, val: int = 0, next: Optional["ListNode"] = None):
        self.val = val
        self.next = next

    def __repr__(self) -> str:
        return f"ListNode({linked_list_to_list(self)})"


class TreeNode:
    def __init__(self, val: int = 0, left: Optional["TreeNode"] = None, right: Optional["TreeNode"] = None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"TreeNode({tree_to_list(self)})"


def linked_list_from_list(values: Optional[list]) -> Optional[ListNode]:
    head: Optional[ListNode] = None
    for value in reversed(values or []):
        head = ListNode(value, head)
    return head


def linked_list_to_list(head: Optional[ListNode], limit: int = 100_000) -> list:
    """Stops after `limit` nodes, so a list that loops back on itself cannot hang the judge."""
    values, node = [], head
    while node is not None and len(values) < limit:
        values.append(node.val)
        node = node.next
    return values


def tree_from_list(values: Optional[list]) -> Optional[TreeNode]:
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue, index = deque([root]), 1
    while queue and index < len(values):
        node = queue.popleft()
        for side in ("left", "right"):
            if index < len(values):
                if values[index] is not None:
                    child = TreeNode(values[index])
                    setattr(node, side, child)
                    queue.append(child)
                index += 1
    return root


def tree_to_list(root: Optional[TreeNode]) -> list:
    """Level order with None for missing children, trailing Nones trimmed, as LeetCode prints it."""
    values: list[Any] = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            values.append(None)
            continue
        values.append(node.val)
        queue.append(node.left)
        queue.append(node.right)
    while values and values[-1] is None:
        values.pop()
    return values
