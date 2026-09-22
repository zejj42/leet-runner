# 75. Sort Colors

<span class="badge medium">Medium</span> <span class="where">array · First 75 · V · Finding Rhythm</span>

<https://leetcode.com/problems/sort-colors/>

You get a list `nums` of `n` objects, each one red, white or blue. Rearrange the list **in place** so that objects of one colour sit together, reds first, then whites, then blues.

The colours are written as numbers: `0` is red, `1` is white and `2` is blue.

Do not call the library's sort. Nothing is returned; the list itself is what gets judged.

**Example 1:**

> **Input:** `nums = [2,0,2,1,1,0]`  
> **Output:** `[0,0,1,1,2,2]`  
> **Explanation:** Two of each colour: the 0s go first, the 1s next, the 2s last.  

**Example 2:**

> **Input:** `nums = [2,0,1]`  
> **Output:** `[0,1,2]`  
> **Explanation:** One of each colour, put in the order 0, 1, 2.  

**Constraints:**

 - `n == nums.length`
 - `1 <= n <= 300`
 - `nums[i]` is either 0, 1, or 2.
