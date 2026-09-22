# 759. Employee Free Time

<span class="badge hard">Hard</span> <span class="where">array · Beyond 75 · XVIII · Heavy Lifting</span>

<https://leetcode.com/problems/employee-free-time/>

`schedule` holds the working hours of a group of employees. `schedule[i]` is the list of employee `i`'s working intervals, each one `[start, end]`. One employee's intervals never overlap each other, and they come sorted by start.

Find the stretches of time when **nobody** is working: return *the list of finite intervals, each longer than zero, during which every employee is free*, sorted by start. The time before the first interval of all and after the last one of all goes on forever, so it is not part of the answer. Two working intervals that touch, like `[1,3]` and `[3,5]`, leave no free time between them.

LeetCode hands this problem `Interval` objects. Here an interval is a plain `[start, end]` list, going in and coming out.

**Example 1:**

> **Input:** `schedule = [[[1,2],[5,6]],[[1,3]],[[4,10]]]`  
> **Output:** `[[3,4]]`  
> **Explanation:** Everybody is free from 3 to 4. They are also free before 1 and after 10, but those stretches never end, so they are left out.  

**Example 2:**

> **Input:** `schedule = [[[1,3],[6,7]],[[2,4]],[[2,5],[9,12]]]`  
> **Output:** `[[5,6],[7,9]]`  

**Constraints:**

 - `1 <= schedule.length <= 50`
 - `1 <= schedule[i].length <= 50`
 - `0 <= start < end <= 10^8`
