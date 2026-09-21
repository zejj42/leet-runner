# 232. Implement Queue using Stacks

<span class="badge easy">Easy</span> <span class="where">stack · First 75 · I · Warm-Up</span>

<https://leetcode.com/problems/implement-queue-using-stacks/>

Build a first in first out (FIFO) queue using only two stacks. Your queue must handle all the standard operations: `push`, `peek`, `pop`, and `empty`.

Create the `MyQueue` class:

 - `void push(int x)` Add element x to the back of the queue.
 - `int pop()` Remove the element at the front and return it.
 - `int peek()` Get the element at the front without removing it.
 - `boolean empty()` Return `true` if the queue is empty, `false` otherwise.

**Notes:**

 - You can **only** use standard stack operations: `push to top`, `peek/pop from top`, `size`, and `is empty`.
 - Your language may not have a built-in stack. You can simulate one with a list or deque, but only use stack operations on it.

**Example 1:**

> **Calls:** `["MyQueue", "push", "push", "peek", "pop", "empty"]`  
> **Arguments:** `[[], [1], [2], [], [], []]`  
> **Output:** `[null, null, null, 1, 1, false]`  
> **Explanation:** Create a new queue. Push 1, then push 2. Peek returns 1. Pop returns 1 and removes it. Empty returns false because one element remains.  

**Constraints:**

 - `1 <= x <= 9`
 - There will be at most `100` calls total to the four methods.
 - `pop` and `peek` are only called when the queue is not empty.
