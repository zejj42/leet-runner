# Minimum Shipping Capacity

<span class="badge medium">Medium</span> <span class="where">binary search · Off-list</span>

A warehouse ships `n` kinds of product. It has `quantities[i]` items of kind `i`, and each one weighs `weights[i]`.

Items go out in boxes, and a box holds items of one kind only. Every box has the same capacity, `c`: it takes at most `c` items, and it may not weigh more than `maxWeightPerBox` in total. There are `maxBoxes` boxes to spare.

Return *the smallest capacity `c` that gets every item shipped* within `maxBoxes` boxes.

**Example 1:**

> **Input:** `quantities = [8,12,5], weights = [2,3,1], maxBoxes = 6, maxWeightPerBox = 20`  
> **Output:** `5`  
> **Explanation:** With `c = 5` the first kind needs 2 boxes, the second 3 and the third 1: 6 in all, and no box weighs more than 15. With `c = 4` it would take 7 boxes.  

**Example 2:**

> **Input:** `quantities = [10,15,8], weights = [5,2,3], maxBoxes = 10, maxWeightPerBox = 15`  
> **Output:** `4`  
> **Explanation:** A box of the first kind may hold 4 items by count but only 3 by weight (4 × 5 = 20 is too heavy), so that kind needs 4 boxes; the second needs 4 and the third 2: 10 in all.  

**Constraints:**

 - `1 <= n <= 10^4`
 - `1 <= quantities[i] <= 10^9`
 - `1 <= weights[i] <= maxWeightPerBox <= 10^9`
 - `1 <= maxBoxes <= 10^9`
 - There are always enough boxes for a capacity of `max(quantities)`.
