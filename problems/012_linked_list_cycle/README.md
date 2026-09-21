# 141. Linked List Cycle

<span class="badge easy">Easy</span> <span class="where">linkedList · First 75 · I · Warm-Up</span>

<https://leetcode.com/problems/linked-list-cycle/>

`head` is the first node of a linked list. Work out whether the list loops back on itself.

A list has a cycle when following `next` over and over brings you back to a node you have already been at. The examples write this with `pos`: the index of the node that the last node's `next` points to, or `-1` when it points nowhere. **`pos` only describes the input; your method is not given it.**

Return `true` *when the list has a cycle*, and `false` when it does not.

**Example 1:**

![](https://assets.leetcode.com/uploads/2018/12/07/circularlinkedlist.png)

> **Input:** `head = [3,2,0,-4], pos = 1`  
> **Output:** `true`  
> **Explanation:** The last node links back to the node at index 1 (counting from 0), so the list loops.  

**Example 2:**

![](https://assets.leetcode.com/uploads/2018/12/07/circularlinkedlist_test2.png)

> **Input:** `head = [1,2], pos = 0`  
> **Output:** `true`  
> **Explanation:** The last node links back to the first one.  

**Example 3:**

![](https://assets.leetcode.com/uploads/2018/12/07/circularlinkedlist_test3.png)

> **Input:** `head = [1], pos = -1`  
> **Output:** `false`  
> **Explanation:** The only node points nowhere: no loop.  

**Constraints:**

 - The list has between `0` and `10^4` nodes.
 - `-10^5 <= Node.val <= 10^5`
 - `pos` is `-1`, or a **real index** in the list.
