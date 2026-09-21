# 32. Longest Valid Parentheses

<span class="badge hard">Hard</span> <span class="where">stack · Beyond 75 · XVIII · Heavy Lifting</span>

<https://leetcode.com/problems/longest-valid-parentheses/>

You get a string with only parentheses characters: `'('` and `')'`. Find and return *the length of the longest valid (balanced) contiguous substring of parentheses*.

**Example 1:**

> **Input:** `s = "(()"`  
> **Output:** `2`  
> **Explanation:** In "(())", the substring "()" has length 2 and is valid. That's the longest.  

**Example 2:**

> **Input:** `s = ")()())"`  
> **Output:** `4`  
> **Explanation:** In ")()())", the substring "()()" has length 4 and is valid. That's the longest.  

**Example 3:**

> **Input:** `s = ""`  
> **Output:** `0`  

**Constraints:**

 - `0 <= s.length <= 3 * 10^4`
 - `s[i]` is `'('`, or `')'`.
