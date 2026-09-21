# 227. Basic Calculator II

<span class="badge medium">Medium</span> <span class="where">stack · Beyond 75 · XVI · Closing the Mediums</span>

<https://leetcode.com/problems/basic-calculator-ii/>

You get a string `s` with a mathematical expression. Evaluate it and return *the result*.

Division truncates toward zero.

You can assume the expression is always valid. All intermediate values stay within `[-2^31, 2^31 - 1]`.

**Note:** You cannot use built-in functions that evaluate expressions as strings, like `eval()`.** Example 1:**

> **Input:** `s = "3+2*2"`  
> **Output:** `7`  

**Example 2:**

> **Input:** `s = " 3/2 "`  
> **Output:** `1`  

**Example 3:**

> **Input:** `s = " 3+5 / 2 "`  
> **Output:** `5`  

**Constraints:**

 - `1 <= s.length <= 3 * 10^5`
 - The string has integers and operators `('+', '-', '*', '/')` separated by spaces.
 - The expression is always valid.
 - All numbers in the expression are non-negative and fit in the range `[0, 2^31 - 1]`.
 - The result always fits in a **32-bit integer**.
