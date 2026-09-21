"""leetkit: the judge, the node types and the scaffolding behind this practice repo."""

from .structures import ListNode, TreeNode, linked_list_from_list, linked_list_to_list, tree_from_list, tree_to_list

__all__ = ["ListNode", "TreeNode", "linked_list_from_list", "linked_list_to_list", "tree_from_list", "tree_to_list",
           "problem_tests"]


def problem_tests(test_file: str):
    from .pytest_glue import problem_tests as build      # pytest is only needed when tests run
    return build(test_file)
