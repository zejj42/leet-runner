# 153. Find Minimum in Rotated Sorted Array

<span class="badge medium">Medium</span> <span class="where">binarySearch · Beyond 75 · XVI · Closing the Mediums</span>

<https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/>

Take a list of `n` numbers in ascending order and **rotate** it somewhere between `1` and `n` times. The list `nums = [0,1,2,4,5,6,7]`, for instance, could turn into:

 - `[4,5,6,7,0,1,2]` after `4` rotations.
 - `[0,1,2,4,5,6,7]` after `7` rotations, which brings it back to where it started.

One **rotation** moves the last element to the front: `[a[0], a[1], a[2], ..., a[n-1]]` becomes `[a[n-1], a[0], a[1], a[2], ..., a[n-2]]`.

You get such a list, `nums`, in which no value appears twice. Return *its smallest element*.

**Example 1:**

> **Input:** `nums = [3,4,5,1,2]`  
> **Output:** `1`  
> **Explanation:** This is [1,2,3,4,5] after 3 rotations.  

**Example 2:**

> **Input:** `nums = [4,5,6,7,0,1,2]`  
> **Output:** `0`  
> **Explanation:** This is [0,1,2,4,5,6,7] after 4 rotations.  

**Example 3:**

> **Input:** `nums = [11,13,15,17]`  
> **Output:** `11`  
> **Explanation:** This is [11,13,15,17] after 4 rotations, so it is in order again.  

**Constraints:**

 - `n == nums.length`
 - `1 <= n <= 5000`
 - `-5000 <= nums[i] <= 5000`
 - No two values in `nums` are the same.
 - `nums` is a sorted list that was rotated between `1` and `n` times.
