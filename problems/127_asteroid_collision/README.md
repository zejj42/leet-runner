# 735. Asteroid Collision

<span class="badge medium">Medium</span> <span class="where">stack · Beyond 75 · XIV · Deeper Still</span>

<https://leetcode.com/problems/asteroid-collision/>

You get an array `asteroids` of integers. Each integer represents one asteroid; its position in the array is its position in space.

Each asteroid's absolute value is its size. Positive values move right, negative values move left. All asteroids move at the same speed.

When asteroids collide, the smaller one explodes. If they're the same size, both explode. Asteroids moving in the same direction never collide. Return the state of all asteroids after all collisions are done.

**Example 1:**

> **Input:** `asteroids = [5,10,-5]`  
> **Output:** `[5,10]`  
> **Explanation:** The asteroid 10 (moving right) collides with -5 (moving left), and the -5 explodes. The 5 and 10 move in the same direction (right), so they never meet.  

**Example 2:**

> **Input:** `asteroids = [8,-8]`  
> **Output:** `[]`  
> **Explanation:** The asteroids have equal size (8 and -8) and opposite directions. Both explode.  

**Example 3:**

> **Input:** `asteroids = [10,2,-5]`  
> **Output:** `[10]`  
> **Explanation:** The 2 (right) and -5 (left) collide; 2 is smaller so it explodes, leaving -5. Then 10 (right) and -5 (left) collide; 10 is larger so -5 explodes.  

**Example 4:**

> **Input:** `asteroids = [3,5,-6,2,-1,4]​​​​​​​`  
> **Output:** `[-6,2,4]`  
> **Explanation:** The -6 (left) collides with 5 and 3, destroying both while continuing left. The 2 (right) collides with -1 (left), destroying -1. The 2 and 4 both move right, so they don't collide.  

**Constraints:**

 - `2 <= asteroids.length <= 10^4`
 - `-1000 <= asteroids[i] <= 1000`
 - `asteroids[i] != 0`
