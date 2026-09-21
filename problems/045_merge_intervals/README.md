# 56. Merge Intervals

<span class="badge medium">Medium</span> <span class="where">array · First 75 · V · Finding Rhythm</span>

<https://leetcode.com/problems/merge-intervals/>

You get a list of `intervals` where each `intervals[i] = [start_i, end_i]`. Merge all overlapping intervals and return *a list of non-overlapping intervals that covers all the input intervals*.

**Example 1:**

> **Input:** `intervals = [[1,3],[2,6],[8,10],[15,18]]`  
> **Output:** `[[1,6],[8,10],[15,18]]`  
> **Explanation:** The intervals [1,3] and [2,6] overlap, so merge them into [1,6].  

**Example 2:**

> **Input:** `intervals = [[1,4],[4,5]]`  
> **Output:** `[[1,5]]`  
> **Explanation:** The intervals [1,4] and [4,5] overlap because they share the point 4.  

**Example 3:**

> **Input:** `intervals = [[4,7],[1,4]]`  
> **Output:** `[[1,7]]`  
> **Explanation:** The intervals [1,4] and [4,7] overlap because they share the point 4.  

**Constraints:**

 - `1 <= intervals.length <= 10^4`
 - `intervals[i].length == 2`
 - `0 <= start_i <= end_i <= 10^4`
