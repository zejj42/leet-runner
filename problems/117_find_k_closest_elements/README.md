# 658. Find K Closest Elements

<span class="badge medium">Medium</span> <span class="where">heap · Beyond 75 · XIII · Keeping Rhythm</span>

<https://leetcode.com/problems/find-k-closest-elements/>

You get a **sorted** list of integers, `arr`, and two integers, `k` and `x`. Return the `k` values of the list that lie nearest to `x`, themselves in ascending order.

`a` counts as nearer to `x` than `b` when either of these holds (so of two values equally far from `x`, the smaller one is the nearer):

 - `|a - x| < |b - x|`, or
 - `|a - x| == |b - x|` and `a < b`

**Example 1:**

> **Input:** `arr = [1,2,3,4,5], k = 4, x = 3`  
> **Output:** `[1,2,3,4]`  

**Example 2:**

> **Input:** `arr = [1,1,2,3,4,5], k = 4, x = -1`  
> **Output:** `[1,1,2,3]`  

**Constraints:**

 - `1 <= k <= arr.length`
 - `1 <= arr.length <= 10^4`
 - `arr` runs in **ascending** order.
 - `-10^4 <= arr[i], x <= 10^4`
