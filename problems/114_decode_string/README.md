# 394. Decode String

<span class="badge medium">Medium</span> <span class="where">stack · Beyond 75 · XII · Building Higher</span>

<https://leetcode.com/problems/decode-string/>

You get an encoded string. Decode it and return the result.

The encoding rule is `k[encoded_string]`. The `encoded_string` inside the brackets repeats exactly `k` times. `k` is always a positive integer.

The input is always valid: no extra whitespace, brackets are balanced, etc. The original data has no digits; digits only appear as repeat counts `k`. So you won't see patterns like `3a` or `2[4]`.

The decoded output will not be longer than `10^5` characters.

**Example 1:**

> **Input:** `s = "3[a]2[bc]"`  
> **Output:** `"aaabcbc"`  

**Example 2:**

> **Input:** `s = "3[a2[c]]"`  
> **Output:** `"accaccacc"`  

**Example 3:**

> **Input:** `s = "2[abc]3[cd]ef"`  
> **Output:** `"abcabccdcdcdef"`  

**Constraints:**

 - `1 <= s.length <= 30`
 - The string has lowercase English letters, digits, and square brackets `'[]'`.
 - The input is always **valid**.
 - Every integer in the string is in the range `[1, 300]`.
