# 904. Fruit Into Baskets

<span class="badge medium">Medium</span> <span class="where">Window · Off-list</span>

<https://leetcode.com/problems/fruit-into-baskets/>

You visit a farm with fruit trees arranged in a row from left to right. An integer list `fruits` represents the trees, where `fruits[i]` is the **type** of fruit the `i^th` tree produces.

You want to collect as much fruit as possible, but there are rules:

 - You have **two** baskets, and each holds only one **fruit type**. Each basket's capacity is unlimited.
 - Starting at any tree, pick **exactly one fruit** from **every** tree as you move right (including the start tree). Each fruit must fit in one of your baskets.
 - Stop when you reach a tree with fruit that doesn't fit in either basket.

Given the list `fruits`, return *the **maximum** number of fruits you can pick*.

**Example 1:**

> **Input:** `fruits = [1,2,1]`  
> **Output:** `3`  
> **Explanation:** Pick all 3 fruits.  

**Example 2:**

> **Input:** `fruits = [0,1,2,2]`  
> **Output:** `3`  
> **Explanation:** You can pick the 3 fruits [1,2,2].  
> Starting at the first tree, you'd only pick the 2 fruits [0,1].  

**Example 3:**

> **Input:** `fruits = [1,2,3,2,2]`  
> **Output:** `4`  
> **Explanation:** Pick the 4 fruits [2,3,2,2].  
> Starting at the first tree, you'd only pick the 2 fruits [1,2].  

**Constraints:**

 - `1 <= fruits.length <= 10^5`
 - `0 <= fruits[i] < fruits.length`
