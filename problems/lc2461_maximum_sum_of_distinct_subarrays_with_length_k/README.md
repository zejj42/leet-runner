# 2461. Maximum Sum of Distinct Subarrays With Length K

<span class="badge medium">Medium</span> <span class="where">Window · Off-list</span>

<https://leetcode.com/problems/maximum-sum-of-distinct-subarrays-with-length-k/>

You get a list of integers, `nums`, and an integer `k`. Look at every subarray of `nums` that satisfies both of these:

 - it is exactly `k` long, and
 - no value appears in it twice: its elements are all **distinct**.

Return *the largest sum any of those subarrays has*. When no subarray satisfies both, return `0`.

*A **subarray** is a run of one or more elements that sit next to each other in the list.*

**Example 1:**

> **Input:** `nums = [1,5,4,2,9,9,9], k = 3`  
> **Output:** `15`  
> **Explanation:** The runs of three are [1,5,4], [5,4,2], [4,2,9], [2,9,9] and [9,9,9]. The last two repeat a 9, so they are out. Of the rest, [4,2,9] has the largest sum, 15.  

**Example 2:**

> **Input:** `nums = [4,4,4], k = 3`  
> **Output:** `0`  
> **Explanation:** The only run of three is [4,4,4], and it repeats the 4. Nothing qualifies, so the answer is 0.  

**Constraints:**

 - `1 <= k <= nums.length <= 10^5`
 - `1 <= nums[i] <= 10^5`
