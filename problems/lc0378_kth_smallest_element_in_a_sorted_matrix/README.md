# 378. Kth Smallest Element in a Sorted Matrix

<span class="badge medium">Medium</span> <span class="where">Binary Search · Off-list</span>

<https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/>

You get an `n x n` `matrix` where each row and column is sorted in ascending order. Return *the* `k^th` *smallest element in the matrix*.

The `k^th` smallest means the `k^th` in sorted order of all elements—if an element appears twice, you count both copies.

**Example 1:**

> **Input:** `matrix = [[1,5,9],[10,11,13],[12,13,15]], k = 8`  
> **Output:** `13`  
> **Explanation:** Sorting all elements gives [1,5,9,10,11,12,13,13,15]. The 8th smallest is 13.  

**Example 2:**

> **Input:** `matrix = [[-5]], k = 1`  
> **Output:** `-5`  

**Constraints:**

 - `n == matrix.length == matrix[i].length`
 - `1 <= n <= 300`
 - `-10^9 <= matrix[i][j] <= 10^9`
 - Each row and column of `matrix` is sorted in non-decreasing order.
 - `1 <= k <= n^2`
