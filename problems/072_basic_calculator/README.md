# 224. Basic Calculator

<span class="badge hard">Hard</span> <span class="where">stack · First 75 · VIII · Heavy Lifting</span>

<https://leetcode.com/problems/basic-calculator/>

You get a string `s` with a valid mathematical expression. Write a calculator that evaluates it and returns *the result*.

**Note:** You cannot use built-in functions that evaluate expressions as strings, like `eval()`.

**Example 1:**

> **Input:** `s = "1 + 1"`  
> **Output:** `2`  

**Example 2:**

> **Input:** `s = " 2-1 + 2 "`  
> **Output:** `3`  

**Example 3:**

> **Input:** `s = "(1+(4+5+2)-3)+(6+8)"`  
> **Output:** `23`  

**Constraints:**

 - `1 <= s.length <= 3 * 10^5`
 - `s` consists of digits, `'+'`, `'-'`, `'('`, `')'`, and `' '`.
 - The expression is always valid.
 - `'+'` cannot be unary (e.g., `"+1"` or `"+(2 + 3)"` won't appear).
 - `'-'` can be unary (e.g., `"-1"` and `"-(2 + 3)"` are allowed).
 - No two operators appear consecutively.
 - All values and intermediate results fit in a 32-bit signed integer.
