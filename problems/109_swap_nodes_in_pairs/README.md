# 24. Swap Nodes in Pairs

<span class="badge medium">Medium</span> <span class="where">linkedList · Beyond 75 · XII · Building Higher</span>

<https://leetcode.com/problems/swap-nodes-in-pairs/>

Take a linked list two nodes at a time, and swap the nodes of each pair: the first with the second, the third with the fourth, and so on. A node left without a partner at the end stays where it is. Return the head of the result.

Leave the values inside the nodes alone: it is the nodes that move, by changing their links.

**Example 1:**

> **Input:** `head = [1,2,3,4]`  
> **Output:** `[2,1,4,3]`  

![](https://assets.leetcode.com/uploads/2020/10/03/swap_ex1.jpg)

**Example 2:**

> **Input:** `head = []`  
> **Output:** `[]`  

**Example 3:**

> **Input:** `head = [1]`  
> **Output:** `[1]`  

**Example 4:**

> **Input:** `head = [1,2,3]`  
> **Output:** `[2,1,3]`  

**Constraints:**

 - The list has between `0` and `100` nodes.
 - `0 <= Node.val <= 100`
