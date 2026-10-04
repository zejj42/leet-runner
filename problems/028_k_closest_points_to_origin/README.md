# 973. K Closest Points to Origin

<span class="badge medium">Medium</span> <span class="where">heap · First 75 · III · Stepping Up</span>

<https://leetcode.com/problems/k-closest-points-to-origin/>

You get a list `points`, in which `points[i] = [x_i, y_i]` is a point on the **X-Y** plane, and an integer `k`. Return the `k` points that lie nearest to the origin `(0, 0)`.

Nearness is measured in a straight line, the Euclidean distance: `√(x_1 - x_2)^2 + (y_1 - y_2)^2` between two points.

The points may come back in **any order**. Which `k` points they are is never in doubt: every input is built so that the answer is **unique**, apart from its order.

**Example 1:**

![](https://assets.leetcode.com/uploads/2021/03/03/closestplane1.jpg)

> **Input:** `points = [[1,3],[-2,2]], k = 1`  
> **Output:** `[[-2,2]]`  
> **Explanation:** (1, 3) lies sqrt(10) from the origin and (-2, 2) lies sqrt(8). sqrt(8) is the smaller, and with k = 1 that one point is the whole answer.  

**Example 2:**

> **Input:** `points = [[3,3],[5,-1],[-2,4]], k = 2`  
> **Output:** `[[3,3],[-2,4]]`  
> **Explanation:** [[-2,4],[3,3]] is the same answer in another order, and is just as good.  

**Constraints:**

 - `1 <= k <= points.length <= 10^4`
 - `-10^4 <= x_i, y_i <= 10^4`
