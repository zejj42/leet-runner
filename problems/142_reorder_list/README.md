# 143. Reorder List

<span class="badge medium">Medium</span> <span class="where">linkedList · Beyond 75 · XVI · Closing the Mediums</span>

<https://leetcode.com/problems/reorder-list/>

You get the head of a singly linked list. Number its nodes from the front:

```
L0 → L1 → … → Ln - 1 → Ln
```

*Rearrange the same list so that it goes first, last, second, second to last, and so on:*

```
L0 → Ln → L1 → Ln - 1 → L2 → Ln - 2 → …
```

Leave the values inside the nodes alone: move the nodes, by changing their links. Nothing is returned; the list itself is what gets judged.

**Example 1:**

![](https://assets.leetcode.com/uploads/2021/03/04/reorder1linked-list.jpg)

> **Input:** `head = [1,2,3,4]`  
> **Output:** `[1,4,2,3]`  

**Example 2:**

![](https://assets.leetcode.com/uploads/2021/03/09/reorder2-linked-list.jpg)

> **Input:** `head = [1,2,3,4,5]`  
> **Output:** `[1,5,2,4,3]`  

**Constraints:**

 - The list has between `1` and `5 * 10^4` nodes.
 - `1 <= Node.val <= 1000`
