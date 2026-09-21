# 424. Longest Repeating Character Replacement

<span class="badge medium">Medium</span> <span class="where">string · Beyond 75 · XIII · Keeping Rhythm</span>

<https://leetcode.com/problems/longest-repeating-character-replacement/>

You get a string `s` and an integer `k`. You can pick any character in the string and change it to any other uppercase English letter. You can do this at most `k` times.

Return *the length of the longest substring of identical characters you can create after these changes*.

**Example 1:**

> **Input:** `s = "ABAB", k = 2`  
> **Output:** `4`  
> **Explanation:** Change both 'A's to 'B's, or both 'B's to 'A's.  

**Example 2:**

> **Input:** `s = "AABABBA", k = 1`  
> **Output:** `4`  
> **Explanation:** Change the 'A' in the middle to 'B' to get "AABBBBA".  
> The substring "BBBB" has the longest run of identical letters, which is 4.  
> Other solutions are possible too.  

**Constraints:**

 - `1 <= s.length <= 10^5`
 - The string `s` contains only uppercase English letters.
 - `0 <= k <= s.length`
