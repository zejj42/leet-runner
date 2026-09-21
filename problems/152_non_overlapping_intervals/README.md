# 435. Non-overlapping Intervals

<span class="badge medium">Medium</span> <span class="where">array · Beyond 75 · XVII · Loose Ends</span>

<https://leetcode.com/problems/non-overlapping-intervals/>

You get a list of intervals, `intervals`, where `intervals[i] = [start_i, end_i]`. Return *the minimum number of intervals to remove so the rest don't overlap*.

**Note:** Intervals that touch at exactly one point are **non-overlapping**. For example, `[1, 2]` and `[2, 3]` don't overlap.

**Example 1:**

> **Input:** `intervals = [[1,2],[2,3],[3,4],[1,3]]`  
> **Output:** `1`  
> **Explanation:** Remove [1,3] and the remaining intervals don't overlap.  

**Example 2:**

> **Input:** `intervals = [[1,2],[1,2],[1,2]]`  
> **Output:** `2`  
> **Explanation:** Remove two [1,2] intervals to make the rest non-overlapping.  

**Example 3:**

> **Input:** `intervals = [[1,2],[2,3]]`  
> **Output:** `0`  
> **Explanation:** No intervals need to be removed—they're already non-overlapping.  

**Constraints:**

 - `1 <= intervals.length <= 10^5`
 - `intervals[i].length == 2`
 - `-5 * 10^4 <= start_i < end_i <= 5 * 10^4`
