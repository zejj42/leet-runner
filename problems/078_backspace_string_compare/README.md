# 844. Backspace String Compare

<span class="badge easy">Easy</span> <span class="where">stack · Beyond 75 · IX · Second Wind</span>

<https://leetcode.com/problems/backspace-string-compare/>

You get two strings `s` and `t`. Treat `'#'` as a backspace character. Return `true` *if they become the same after processing all backspaces*.

If you backspace when the text is empty, nothing happens.

**Example 1:**

> **Input:** `s = "ab#c", t = "ad#c"`  
> **Output:** `true`  
> **Explanation:** `s = "ab#c"` becomes `"ac"`. `t = "ad#c"` also becomes `"ac"`.  

**Example 2:**

> **Input:** `s = "ab##", t = "c#d#"`  
> **Output:** `true`  
> **Explanation:** `s = "ab##"` backspaces to empty. `t = "c#d#"` also backspaces to empty.  

**Example 3:**

> **Input:** `s = "a#c", t = "b"`  
> **Output:** `false`  
> **Explanation:** `s = "a#c"` becomes `"c"`. `t = "b"` stays `"b"`. They're different.  

**Constraints:**

 - `1 <= s.length, t.length <= 200`
 - Both strings contain only lowercase letters and `'#'` characters.
