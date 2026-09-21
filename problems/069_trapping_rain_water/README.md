# 42. Trapping Rain Water

<span class="badge hard">Hard</span> <span class="where">stack · First 75 · VIII · Heavy Lifting</span>

<https://leetcode.com/problems/trapping-rain-water/>

You get `n` non-negative integers `height` that map out terrain elevation. Each bar has width 1. Calculate how much water gets trapped after it rains.

**Example 1:**

![](https://assets.leetcode.com/uploads/2018/10/22/rainwatertrap.png)

> **Input:** `height = [0,1,0,2,1,0,1,3,2,1,2,1]`  
> **Output:** `6`  
> **Explanation:** The height array [0,1,0,2,1,0,1,3,2,1,2,1] represents the terrain. Water fills the valleys; here, 6 units get trapped.  

**Example 2:**

> **Input:** `height = [4,2,0,3,2,5]`  
> **Output:** `9`  

**Constraints:**

 - `n == height.length`
 - `1 <= n <= 2 * 10^4`
 - `0 <= height[i] <= 10^5`
