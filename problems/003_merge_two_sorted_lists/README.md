# 21. Merge Two Sorted Lists

<span class="badge easy">Easy</span> <span class="where">linkedList · First 75 · I · Warm-Up</span>

<https://leetcode.com/problems/merge-two-sorted-lists/>

You get `list1` and `list2`: the heads of two linked lists, each already sorted.

Join them into a single **sorted** list. Build it out of the nodes the two lists already have, linked together in the right order.

Return *the head of that joined list*.

**Example 1:**

![](https://assets.leetcode.com/uploads/2020/10/03/merge_ex1.jpg)

> **Input:** `list1 = [1,2,4], list2 = [1,3,4]`  
> **Output:** `[1,1,2,3,4,4]`  

**Example 2:**

> **Input:** `list1 = [], list2 = []`  
> **Output:** `[]`  

**Example 3:**

> **Input:** `list1 = [], list2 = [0]`  
> **Output:** `[0]`  

**Constraints:**

 - Each list has between `0` and `50` nodes.
 - `-100 <= Node.val <= 100`
 - `list1` and `list2` each run in **non-decreasing** order.
