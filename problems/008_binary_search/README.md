# 704. Binary Search

<span class="badge easy">Easy</span> <span class="where">binarySearch · First 75 · I · Warm-Up</span>

<https://leetcode.com/problems/binary-search/>

You get a sorted list of integers, `nums`, and an integer `target`. Search for `target` in the list. If it exists, return its index. Otherwise, return `-1`.

**Example 1:**

> **Input:** `nums = [-1,0,3,5,9,12], target = 9`  
> **Output:** `4`  
> **Explanation:** The number 9 is in the list at index 4.  

**Example 2:**

> **Input:** `nums = [-1,0,3,5,9,12], target = 2`  
> **Output:** `-1`  
> **Explanation:** The number 2 is not in the list, so return -1.  

**Constraints:**

 - `1 <= nums.length <= 10^4`
 - `-10^4 < nums[i], target < 10^4`
 - Each number in `nums` is **different from all others**.
 - The list is sorted in ascending order.
