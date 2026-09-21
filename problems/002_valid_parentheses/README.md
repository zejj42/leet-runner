# 20. Valid Parentheses

<span class="badge easy">Easy</span> <span class="where">stack · First 75 · I · Warm-Up</span>

<https://leetcode.com/problems/valid-parentheses/>

You're given a string `s` with only these bracket characters: `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`. Check whether the string is valid.

A string is valid when:

 1. Each closing bracket matches the type of its opening bracket.
 2. Brackets close in the correct order.
 3. Every closing bracket has a matching opening bracket of the same type.

**Example 1:**

> **Input:** `s = "()"`  
> **Output:** `true`  

**Example 2:**

> **Input:** `s = "()[]{}"`  
> **Output:** `true`  

**Example 3:**

> **Input:** `s = "(]"`  
> **Output:** `false`  

**Example 4:**

> **Input:** `s = "([])"`  
> **Output:** `true`  

**Example 5:**

> **Input:** `s = "([)]"`  
> **Output:** `false`  

**Constraints:**

 - `1 <= s.length <= 10^4`
 - `s` consists of parentheses only `'()[]{}'`.
