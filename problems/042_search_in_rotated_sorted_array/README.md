# 33. Search in Rotated Sorted Array

<span class="badge medium">Medium</span> <span class="where">binarySearch · First 75 · V · Finding Rhythm</span>

<https://leetcode.com/problems/search-in-rotated-sorted-array/>

You get an integer array `nums`, sorted in ascending order, with every value unique.

Before you receive it, the array may have been left-rotated at some unknown index `k` (where `1 <= k < nums.length`). When rotated, the elements from index `k` onward move to the front: `[nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]]` (**0-indexed**). For example, `[0,1,2,4,5,6,7]` rotated left by `3` becomes `[4,5,6,7,0,1,2]`.

You're given the possibly-rotated array and an integer `target`. Return *the index where* `target` *is in* `nums`*, or* `-1` *if it's not there*.

**Example 1:**

> **Input:** `nums = [4,5,6,7,0,1,2], target = 0`  
> **Output:** `4`  

**Example 2:**

> **Input:** `nums = [4,5,6,7,0,1,2], target = 3`  
> **Output:** `-1`  

**Example 3:**

> **Input:** `nums = [1], target = 0`  
> **Output:** `-1`  

**Constraints:**

 - `1 <= nums.length <= 5000`
 - `-10^4 <= nums[i] <= 10^4`
 - All values in `nums` are distinct.
 - `nums` is a sorted array that may have been rotated.
 - `-10^4 <= target <= 10^4`
