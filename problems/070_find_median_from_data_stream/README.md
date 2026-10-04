# 295. Find Median from Data Stream

<span class="badge hard">Hard</span> <span class="where">heap · First 75 · VIII · Heavy Lifting</span>

<https://leetcode.com/problems/find-median-from-data-stream/>

The **median** of a sorted list of integers is the value in its middle. A list of even length has no single middle, so its median is the mean of the two values nearest the middle.

 - `arr = [2,3,4]` has the median `3`.
 - `arr = [2,3]` has the median `(2 + 3) / 2 = 2.5`.

Write the class `MedianFinder`:

 - `MedianFinder()` starts out holding no numbers.
 - `void addNum(int num)` takes in `num`, the next integer of the stream.
 - `double findMedian()` gives the median of everything taken in so far. An answer within `10^-5` of the true one counts as right.

**Example 1:**

> **Calls:** `["MedianFinder", "addNum", "addNum", "findMedian", "addNum", "findMedian"]`  
> **Arguments:** `[[], [1], [2], [], [3], []]`  
> **Output:** `[null, null, null, 1.5, null, 2.0]`  
> **Explanation:** With 1 and 2 taken in, the median is (1 + 2) / 2 = 1.5. Once 3 joins them, the middle value is 2.  

**Constraints:**

 - `-10^5 <= num <= 10^5`
 - `findMedian` is only ever called once at least one number is in.
 - `addNum` and `findMedian` are called at most `5 * 10^4` times between them.
