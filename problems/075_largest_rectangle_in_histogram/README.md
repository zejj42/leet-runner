# 84. Largest Rectangle in Histogram

<span class="badge hard">Hard</span> <span class="where">stack · First 75 · VIII · Heavy Lifting</span>

<https://leetcode.com/problems/largest-rectangle-in-histogram/>

You get an array `heights` representing the heights of histogram bars, each with width 1. Find and return *the area of the largest rectangle that fits in the histogram*.

**Example 1:**

![](https://assets.leetcode.com/uploads/2021/01/04/histogram.jpg)

> **Input:** `heights = [2,1,5,6,2,3]`  
> **Output:** `10`  
> **Explanation:** Each bar in the histogram has width 1. The largest rectangle has area 10 units (height 5, width 2).  

**Example 2:**

![](https://assets.leetcode.com/uploads/2021/01/04/histogram-1.jpg)

> **Input:** `heights = [2,4]`  
> **Output:** `4`  

**Constraints:**

 - `1 <= heights.length <= 10^5`
 - `0 <= heights[i] <= 10^4`
