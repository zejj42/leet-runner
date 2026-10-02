# 1011. Capacity To Ship Packages Within D Days

<span class="badge medium">Medium</span> <span class="where">Binary Search · Off-list</span>

<https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/>

Packages wait in a line on a conveyor belt, and all of them have to reach another port within `days` days.

Package `i` weighs `weights[i]`. Every day the ship is loaded once, with packages taken off the belt in the order they stand in `weights`: no skipping ahead, no reordering. A day's load may not weigh more than the ship's capacity.

Return *the smallest capacity the ship can have* and still get every package across within `days` days.

**Example 1:**

> **Input:** `weights = [1,2,3,4,5,6,7,8,9,10], days = 5`  
> **Output:** `15`  
> **Explanation:** With a capacity of 15 the five days carry (1, 2, 3, 4, 5), (6, 7), (8), (9) and (10). A capacity of 14 would only work by taking packages out of order, such as (2, 3, 4, 5) then (1, 6, 7), and the order is fixed.  

**Example 2:**

> **Input:** `weights = [3,2,2,4,1,4], days = 3`  
> **Output:** `6`  
> **Explanation:** With a capacity of 6 the three days carry (3, 2), (2, 4) and (1, 4). Nothing smaller manages it in three.  

**Example 3:**

> **Input:** `weights = [1,2,3,1,1], days = 4`  
> **Output:** `3`  
> **Explanation:** The four days carry (1), (2), (3) and (1, 1). The package of weight 3 alone rules out anything below 3.  

**Constraints:**

 - `1 <= days <= weights.length <= 5 * 10^4`
 - `1 <= weights[i] <= 500`
