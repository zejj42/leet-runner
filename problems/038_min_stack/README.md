# 155. Min Stack

<span class="badge medium">Medium</span> <span class="where">stack · First 75 · IV · Building Blocks</span>

<https://leetcode.com/problems/min-stack/>

Build a stack that can push, pop, check the top element, and find the minimum value all in constant time.

Create the `MinStack` class:

 - `MinStack()` Set up a new stack.
 - `void push(int value)` Add `value` to the top of the stack.
 - `void pop()` Remove the top element.
 - `int top()` Return the top element without removing it.
 - `int getMin()` Return the smallest element in the stack.

Each method must run in constant time.

**Example 1:**

> **Calls:** `["MinStack","push","push","push","getMin","pop","top","getMin"]`  
> **Arguments:** `[[],[-2],[0],[-3],[],[],[],[]]`  
> **Output:** `[null,null,null,null,-3,null,0,-2]`  
> **Explanation:** Push -2, then 0, then -3 (the new minimum). Call getMin to get -3. Pop to remove -3. Call top to get 0. Call getMin to get -2.  

**Constraints:**

 - `-2^31 <= val <= 2^31 - 1`
 - `pop`, `top`, and `getMin` are only called when the stack is **not empty**.
 - There will be at most `3 * 10^4` calls total to `push`, `pop`, `top`, and `getMin`.
