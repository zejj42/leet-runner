# 1. Two Sum

<span class="badge easy">Easy</span> <span class="where">array · First 75 · I · Warm-Up</span>

<https://leetcode.com/problems/two-sum/>

You get a list of integers, `nums`, and one more integer, `target`. Two of the numbers in the list add up to `target`: return *the indices of those two numbers*.

Every input has ***exactly* one such pair**. The pair is two different positions in the list: one element cannot be counted twice.

The two indices may come back in either order.

**Example 1:**

> **Input:** `nums = [2,7,11,15], target = 9`  
> **Output:** `[0,1]`  
> **Explanation:** `nums[0] + nums[1]` is `2 + 7`, which is 9.  

**Example 2:**

> **Input:** `nums = [3,2,4], target = 6`  
> **Output:** `[1,2]`  

**Example 3:**

> **Input:** `nums = [3,3], target = 6`  
> **Output:** `[0,1]`  

**Constraints:**

 - `2 <= nums.length <= 10^4`
 - `-10^9 <= nums[i] <= 10^9`
 - `-10^9 <= target <= 10^9`
 - **There is one right answer, never more.**
