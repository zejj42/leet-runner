# 895. Maximum Frequency Stack

<span class="badge hard">Hard</span> <span class="where">stack · Beyond 75 · XVIII · Heavy Lifting</span>

<https://leetcode.com/problems/maximum-frequency-stack/>

Build a stack that pushes values and pops the most frequent element.

Create the `FreqStack` class:

 - `FreqStack()` Create an empty frequency stack.
 - `void push(int val)` Add `val` to the stack.
 - `int pop()` Remove and return the most frequent element. If multiple elements tie for most frequent, remove the one closest to the top.

**Example 1:**

> **Calls:** `["FreqStack", "push", "push", "push", "push", "push", "push", "pop", "pop", "pop", "pop"]`  
> **Arguments:** `[[], [5], [7], [5], [7], [4], [5], [], [], [], []]`  
> **Output:** `[null, null, null, null, null, null, null, 5, 7, 5, 4]`  
> **Explanation:** Push 5 and 7 (each frequency 1), then 5 again (frequency 2), then 7 again (frequency 2), then 4 (frequency 1), then 5 again (frequency 3, now the most frequent). Pop returns 5, then 7 (tied at frequency 2 but closer to top), then 5 (most frequent), then 4 (tied but closest to top).  

**Constraints:**

 - `0 <= val <= 10^9`
 - There will be at most `2 * 10^4` calls total to `push` and `pop`.
 - When `pop` is called, the stack is never empty.
