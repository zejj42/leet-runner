# 215. Kth Largest Element in an Array

<span class="badge medium">Medium</span> <span class="where">heap · Beyond 75 · XIV · Deeper Still</span>

<https://leetcode.com/problems/kth-largest-element-in-an-array/>

You get a list of integers, `nums`, and an integer `k`. Return *the* `k^th` *largest element of the list*.

That is the element standing in position `k` once the list is ordered from largest to smallest. Equal values each take a position of their own: it is not the `k^th` distinct value.

**Example 1:**

> **Input:** `nums = [3,2,1,5,6,4], k = 2`  
> **Output:** `5`  

**Example 2:**

> **Input:** `nums = [3,2,3,1,2,4,5,5,6], k = 4`  
> **Output:** `4`  

**Constraints:**

 - `1 <= k <= nums.length <= 10^5`
 - `-10^4 <= nums[i] <= 10^4`
