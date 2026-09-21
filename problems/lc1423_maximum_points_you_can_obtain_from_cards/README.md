# 1423. Maximum Points You Can Obtain from Cards

<span class="badge medium">Medium</span> <span class="where">Window · Off-list</span>

<https://leetcode.com/problems/maximum-points-you-can-obtain-from-cards/>

Cards are arranged in a row, and each card has a point value. The integer list `cardPoints` gives these point values.

You can take one card from the beginning or the end of the row, one at a time. You must take exactly `k` cards.

Your score is the sum of points on the cards you take.

Given the list `cardPoints` and the integer `k`, return the *maximum score* you can achieve.

**Example 1:**

> **Input:** `cardPoints = [1,2,3,4,5,6,1], k = 3`  
> **Output:** `12`  
> **Explanation:** Taking the leftmost card gives 1 point, but taking the rightmost 3 cards gives 1 + 6 + 5 = 12, which is better.  

**Example 2:**

> **Input:** `cardPoints = [2,2,2], k = 2`  
> **Output:** `4`  
> **Explanation:** Any two cards you choose sum to 4.  

**Example 3:**

> **Input:** `cardPoints = [9,7,7,9,7,7,9], k = 7`  
> **Output:** `55`  
> **Explanation:** Take all 7 cards. Your score is the sum of all their points.  

**Constraints:**

 - `1 <= cardPoints.length <= 10^5`
 - `1 <= cardPoints[i] <= 10^4`
 - `1 <= k <= cardPoints.length`
