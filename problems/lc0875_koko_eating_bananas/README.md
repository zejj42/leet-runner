# 875. Koko Eating Bananas

<span class="badge medium">Medium</span> <span class="where">Binary Search · Off-list</span>

<https://leetcode.com/problems/koko-eating-bananas/>

You have `n` piles of bananas. The `i^th` pile has `piles[i]` bananas. The guards will return in `h` hours.

You pick a speed `k` (bananas per hour) and stick to it. Each hour, you pick one pile and eat `k` bananas from it. If the pile has fewer than `k` bananas, you eat the whole pile and don't eat any more that hour.

You want to finish all the bananas before the guards return.

Find *the minimum speed* `k` *so you finish all bananas within* `h` *hours*.

**Example 1:**

> **Input:** `piles = [3,6,7,11], h = 8`  
> **Output:** `4`  

**Example 2:**

> **Input:** `piles = [30,11,23,4,20], h = 5`  
> **Output:** `30`  

**Example 3:**

> **Input:** `piles = [30,11,23,4,20], h = 6`  
> **Output:** `23`  

**Constraints:**

 - `1 <= piles.length <= 10^4`
 - `piles.length <= h <= 10^9`
 - `1 <= piles[i] <= 10^9`
