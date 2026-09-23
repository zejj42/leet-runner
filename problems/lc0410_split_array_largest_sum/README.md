# 410. Split Array Largest Sum

<span class="badge hard">Hard</span> <span class="where">Binary Search · Off-list</span>

<https://leetcode.com/problems/split-array-largest-sum/>

You get an integer array `nums` and an integer `k`. Split `nums` into `k` non-empty subarrays so that the largest sum among all subarrays is as small as possible.

Return *that smallest possible largest sum*.

A **subarray** is any contiguous slice of elements from the array.

**Example 1:**

> **Input:** `nums = [7,2,5,10,8], k = 2`  
> **Output:** `18`  
> **Explanation:** You can split `nums` into two subarrays in several ways. The best is [7,2,5] and [10,8]: their sums are 14 and 18, so the largest is 18.  

**Example 2:**

> **Input:** `nums = [1,2,3,4,5], k = 2`  
> **Output:** `9`  
> **Explanation:** You can split `nums` into two subarrays in several ways. The best is [1,2,3] and [4,5]: their sums are 6 and 9, so the largest is 9.  

**Constraints:**

 - `1 <= nums.length <= 1000`
 - `0 <= nums[i] <= 10^6`
 - `1 <= k <= min(50, nums.length)`
