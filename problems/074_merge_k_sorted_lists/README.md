# 23. Merge k Sorted Lists

<span class="badge hard">Hard</span> <span class="where">heap · First 75 · VIII · Heavy Lifting</span>

<https://leetcode.com/problems/merge-k-sorted-lists/>

You get `lists`, a list of `k` linked lists. Each of them is already sorted, smallest value first.

*Join them all into a single sorted linked list, and return its head.*

**Example 1:**

> **Input:** `lists = [[1,4,5],[1,3,4],[2,6]]`  
> **Output:** `[1,1,2,3,4,4,5,6]`  
> **Explanation:** The three lists 1->4->5, 1->3->4 and 2->6 come out as one: 1->1->2->3->4->4->5->6.  

**Example 2:**

> **Input:** `lists = []`  
> **Output:** `[]`  

**Example 3:**

> **Input:** `lists = [[]]`  
> **Output:** `[]`  

**Constraints:**

 - `k == lists.length`
 - `0 <= k <= 10^4`
 - `0 <= lists[i].length <= 500`
 - `-10^4 <= lists[i][j] <= 10^4`
 - Every `lists[i]` runs in **ascending order**.
 - All the lists together hold at most `10^4` nodes.
