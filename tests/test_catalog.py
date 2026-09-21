"""The list of problems, and the ways to name one."""

import pytest

from leetkit.catalog import all_problems, find

from helpers import problem


def test_the_whole_list_is_here_and_every_folder_name_is_unique():
    problems = all_problems()
    assert len([p for p in problems if p.number]) == 169
    assert len({p.folder.name for p in problems}) == len(problems)
    assert len({p.slug for p in problems}) == len(problems)


@pytest.mark.parametrize("reference", ["1", "001", "two-sum", "two sum", "Two Sum", "TWO-SUM", "001_two_sum"])
def test_a_problem_can_be_named_many_ways(reference):
    assert find(reference).slug == "two-sum"


def test_off_list_problems_are_found_by_their_leetcode_id():
    assert find("lc904").slug == "fruit-into-baskets"


def test_an_ambiguous_or_unknown_name_says_so():
    with pytest.raises(LookupError, match="several"):
        find("tree")
    with pytest.raises(LookupError, match="No problem"):
        find("no such problem anywhere")
