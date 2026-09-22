# 252. Meeting Rooms

<span class="badge easy">Easy</span> <span class="where">array · Beyond 75 · IX · Second Wind</span>

<https://leetcode.com/problems/meeting-rooms/>

You get a list of meetings, `intervals`, where `intervals[i] = [start_i, end_i]` says when meeting `i` starts and when it ends. Work out whether one person can sit through every meeting from start to end.

Return `true` *when no two meetings overlap*, and `false` when any two do. Meetings that only touch do not overlap: one may start at the very moment another ends, like `[1,2]` and `[2,3]`.

**Example 1:**

> **Input:** `intervals = [[0,30],[5,10],[15,20]]`  
> **Output:** `false`  
> **Explanation:** The meeting from 0 to 30 is still going on when the one at 5 begins.  

**Example 2:**

> **Input:** `intervals = [[7,10],[2,4]]`  
> **Output:** `true`  

**Constraints:**

 - `0 <= intervals.length <= 10^4`
 - `intervals[i].length == 2`
 - `0 <= start_i < end_i <= 10^6`
