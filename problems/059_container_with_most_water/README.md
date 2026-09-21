# 11. Container With Most Water

<span class="badge medium">Medium</span> <span class="where">array · First 75 · VII · Rounding Out</span>

<https://leetcode.com/problems/container-with-most-water/>

You get an integer list `height` of length `n`. There are `n` vertical lines: the `i^th` line has endpoints at `(i, 0)` and `(i, height[i])`.

Find two lines that form a container with the x-axis, such that the container holds the most water.

Return *the maximum amount of water any container can hold*.

**Notice:** The container cannot be slanted.

**Example 1:**

![](https://s3-lc-upload.s3.amazonaws.com/uploads/2018/07/17/question_11.jpg)

> **Input:** `height = [1,8,6,2,5,4,8,3,7]`  
> **Output:** `49`  
> **Explanation:** The array [1,8,6,2,5,4,8,3,7] represents the vertical lines shown. The largest area (the blue section) the container can hold is 49.  

**Example 2:**

> **Input:** `height = [1,1]`  
> **Output:** `1`  

**Constraints:**

 - `n == height.length`
 - `2 <= n <= 10^5`
 - `0 <= height[i] <= 10^4`
