# 19. Remove Nth Node From End of List

<span class="badge medium">Medium</span> <span class="where">linkedList · Beyond 75 · XI · Stepping Up Again</span>

<https://leetcode.com/problems/remove-nth-node-from-end-of-list/>

`head` is the first node of a linked list. Take out the node that is `n`th counting from the end (`n = 1` is the last node), and return the head of what is left.

**Example 1:**

![](https://assets.leetcode.com/uploads/2020/10/03/remove_ex1.jpg)

> **Input:** `head = [1,2,3,4,5], n = 2`  
> **Output:** `[1,2,3,5]`  

**Example 2:**

> **Input:** `head = [1], n = 1`  
> **Output:** `[]`  

**Example 3:**

> **Input:** `head = [1,2], n = 1`  
> **Output:** `[1]`  

**Constraints:**

 - The list has `sz` nodes.
 - `1 <= sz <= 30`
 - `0 <= Node.val <= 100`
 - `1 <= n <= sz`
