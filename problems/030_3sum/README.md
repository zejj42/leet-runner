# 15. 3Sum

<span class="badge medium">Medium</span> <span class="where">array · First 75 · III · Stepping Up</span>

<https://leetcode.com/problems/3sum/>

You get an integer list `nums`. Return all triplets `[nums[i], nums[j], nums[k]]` where `i != j`, `i != k`, `j != k`, and `nums[i] + nums[j] + nums[k] == 0`.

The result must not contain duplicate triplets.

**Example 1:**

> **Input:** `nums = [-1,0,1,2,-1,-4]`  
> **Output:** `[[-1,-1,2],[-1,0,1]]`  
> **Explanation:**   
> nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0.  
> nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0.  
> nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0.  
> The two distinct triplets are [-1,0,1] and [-1,-1,2].  
> The order of the triplets and the order of the output list don't matter.  

**Example 2:**

> **Input:** `nums = [0,1,1]`  
> **Output:** `[]`  
> **Explanation:** The only possible triplet doesn't sum to 0.  

**Example 3:**

> **Input:** `nums = [0,0,0]`  
> **Output:** `[[0,0,0]]`  
> **Explanation:** The only possible triplet sums to 0.  

**Constraints:**

 - `3 <= nums.length <= 3000`
 - `-10^5 <= nums[i] <= 10^5`
