# 57. Insert Interval

<span class="badge medium">Medium</span> <span class="where">array · First 75 · III · Stepping Up</span>

<https://leetcode.com/problems/insert-interval/>

You get a list of non-overlapping intervals, `intervals`, where each `intervals[i] = [start_i, end_i]` holds the start and end of that interval. The list is sorted by `start_i` in ascending order. You also get another interval, `newInterval = [start, end]`.

Two intervals overlap if they share **at least** one point.

Insert `newInterval` into `intervals`. Keep `intervals` sorted in ascending order by `start_i` and make sure no intervals overlap—merge them if needed.

Return the updated `intervals`.

**Note:** You don't have to modify `intervals` in place; you can create a new list and return it.

**Example 1:**

> **Input:** `intervals = [[1,3],[6,9]], newInterval = [2,5]`  
> **Output:** `[[1,5],[6,9]]`  

**Example 2:**

> **Input:** `intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]], newInterval = [4,8]`  
> **Output:** `[[1,2],[3,10],[12,16]]`  
> **Explanation:** The new interval [4,8] overlaps with [3,5], [6,7], and [8,10].  

**Constraints:**

 - `0 <= intervals.length <= 10^4`
 - `intervals[i].length == 2`
 - `0 <= start_i <= end_i <= 10^5`
 - The list `intervals` is sorted by `start_i` in **ascending** order.
 - `newInterval.length == 2`
 - `0 <= start <= end <= 10^5`
