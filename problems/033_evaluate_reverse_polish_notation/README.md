# 150. Evaluate Reverse Polish Notation

<span class="badge medium">Medium</span> <span class="where">stack · First 75 · III · Stepping Up</span>

<https://leetcode.com/problems/evaluate-reverse-polish-notation/>

You get an array of strings `tokens` representing an arithmetic expression in Reverse Polish Notation.

Evaluate this expression and return *the integer result*.

**Note** that:

 - Valid operators are `'+'`, `'-'`, `'*'`, and `'/'`.
 - Each operand is an integer or the result of another operation.
 - Division truncates toward zero.
 - You won't encounter division by zero.
 - The input is always a valid expression in reverse polish notation.
 - The result and all intermediate values fit in a **32-bit** integer.** Example 1:**

> **Input:** `tokens = ["2","1","+","3","*"]`  
> **Output:** `9`  
> **Explanation:** The expression is (2 + 1) * 3 = 3 * 3 = 9.  

**Example 2:**

> **Input:** `tokens = ["4","13","5","/","+"]`  
> **Output:** `6`  
> **Explanation:** The expression is 4 + (13 / 5) = 4 + 2 = 6.  

**Example 3:**

> **Input:** `tokens = ["10","6","9","3","+","-11","*","/","*","17","+","5","+"]`  
> **Output:** `22`  
> **Explanation:** Step by step:  
> `9 + 3 = 12`  
> `12 * -11 = -132`  
> `6 / -132 = 0` (truncates toward zero)  
> `10 * 0 = 0`  
> `0 + 17 = 17`  
> `17 + 5 = 22`  

**Constraints:**

 - `1 <= tokens.length <= 10^4`
 - Each element `tokens[i]` is an operator (`"+"`, `"-"`, `"*"`, `"/"`) or an integer in `[-200, 200]`.
