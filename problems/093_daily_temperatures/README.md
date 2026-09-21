# 739. Daily Temperatures

<span class="badge medium">Medium</span> <span class="where">stack · Beyond 75 · X · Firmer Ground</span>

<https://leetcode.com/problems/daily-temperatures/>

You get an array `temperatures` with daily temperatures. For each day, find *how many days ahead you need to wait to see a warmer temperature*. Return this as an array `answer` where `answer[i]` is the wait time for day `i`. If no warmer day is coming, set `answer[i]` to `0`.

**Example 1:**

> **Input:** `temperatures = [73,74,75,71,69,72,76,73]`  
> **Output:** `[1,1,4,2,1,1,0,0]`  

**Example 2:**

> **Input:** `temperatures = [30,40,50,60]`  
> **Output:** `[1,1,1,0]`  

**Example 3:**

> **Input:** `temperatures = [30,60,90]`  
> **Output:** `[1,1,0]`  

**Constraints:**

 - `1 <= temperatures.length <= 10^5`
 - `30 <= temperatures[i] <= 100`
