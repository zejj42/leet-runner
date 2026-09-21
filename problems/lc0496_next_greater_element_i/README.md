# 496. Next Greater Element I

<span class="badge easy">Easy</span> <span class="where">Stack · Off-list</span>

<https://leetcode.com/problems/next-greater-element-i/>

The **next greater element** of an element `x` is the **first element greater** than `x` that appears **to the right** of `x` in the array.

You get two **distinct, 0-indexed** integer lists, `nums1` and `nums2`, where all elements of `nums1` appear in `nums2`.

For each element in `nums1`, find it in `nums2` and determine its **next greater element** in `nums2`. If no greater element exists to the right, return `-1`.

Return *an array `ans` of length `nums1.length` where `ans[i]` is the **next greater element** for `nums1[i]`.*

**Example 1:**

> **Input:** `nums1 = [4,1,2], nums2 = [1,3,4,2]`  
> **Output:** `[-1,3,-1]`  
> **Explanation:** For each value in `nums1`, here's its **next greater element**:  
> - 4 appears at index 2 in `nums2 = [1,3,4,2]`. No element to the right is greater, so the answer is -1.  
> - 1 appears at index 0 in `nums2 = [1,3,4,2]`. The next greater element is 3.  
> - 2 appears at index 3 in `nums2 = [1,3,4,2]`. No element to the right is greater, so the answer is -1.  

**Example 2:**

> **Input:** `nums1 = [2,4], nums2 = [1,2,3,4]`  
> **Output:** `[3,-1]`  
> **Explanation:** For each value in `nums1`, here's its **next greater element**:  
> - 2 appears at index 1 in `nums2 = [1,2,3,4]`. The next greater element is 3.  
> - 4 appears at index 3 in `nums2 = [1,2,3,4]`. No element to the right is greater, so the answer is -1.  

**Constraints:**

 - `1 <= nums1.length <= nums2.length <= 1000`
 - `0 <= nums1[i], nums2[i] <= 10^4`
 - All integers in `nums1` and `nums2` are **different**.
 - Every number in `nums1` appears in `nums2`.
