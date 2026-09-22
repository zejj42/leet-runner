# 611. Valid Triangle Number

<span class="badge medium">Medium</span> <span class="where">Two Pointers · Off-list</span>

<https://leetcode.com/problems/valid-triangle-number/>

You get a list of integers, `nums`. Pick any three of its elements (three different positions) and treat them as the side lengths of a triangle. Return *how many such triples can form a triangle*, that is, how many have every two sides adding up to more than the third.

**Example 1:**

> **Input:** `nums = [2,2,3,4]`  
> **Output:** `3`  
> **Explanation:** Three triples work: 2,3,4 with the first 2, 2,3,4 with the second 2, and 2,2,3. The two 2s count as different positions.  

**Example 2:**

> **Input:** `nums = [4,2,3,4]`  
> **Output:** `4`  

**Constraints:**

 - `1 <= nums.length <= 1000`
 - `0 <= nums[i] <= 1000`
