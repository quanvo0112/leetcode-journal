# 0011. Container With Most Water

- **Problem Link:** https://leetcode.com/problems/container-with-most-water/
- **Difficulty:** `Medium`
- **NeetCode Category:** `Two Pointers`
- **LeetCode Topics:** `Array` / `Two Pointers` / `Greedy`
- **Core Pattern:** `Converging Two Pointers (Shift Shorter Line)`
- **Last Practiced:** 2026-09-20
- **Proficiency Level:** 
  - [x] Level 1: Solved smoothly (< 20 mins, optimal)
  - [ ] Level 2: Struggled / Non-optimal / Edge-case bugs
  - [ ] Level 3: Needed editorial or hints

---

## 1. Pattern Recognition & Triggers

- **Clues in prompt:** *"Find two lines that together with the x-axis form a container, such that the container contains the most water"*, *"Return the maximum amount of water a container can store"*, *"You may not slant the container"*.
- **Core intuition:**
  - The capacity of a container formed between two indices `left` and `right` is strictly defined by:
    $$\text{Area} = \min(height[left], height[right]) \times (right - left)$$
  - The width starts at its maximum possible value when pointers are placed at opposite ends: `left = 0` and `right = n - 1`.
  - As pointers move inward, the width $(right - left)$ monotonically decreases.
  - To compensate for the shrinking width and find a larger area, the bottleneck height ($\min(height[left], height[right])$) **must increase**.
  - If $height[left] < height[right]$, keeping `left` while decrementing `right` can only result in smaller widths with height bounded by $\le height[left]$. Thus, all pairs with the current `left` and any inner `right` are guaranteed to produce smaller areas. We can safely eliminate `left` by advancing `++left`.
  - Conversely, if $height[right] \le height[left]$, we eliminate `right` by decrementing `--right`.

---

## 2. Approach & Trade-offs

1. **Approach 1 — Brute Force ($O(N^2)$ Time, $O(1)$ Space):**
   - Test every possible pair $(i, j)$ with nested loops and calculate the water volume.
   - *Verdict:* With $N = 10^5$, $N^2 = 10^{10}$ operations $\rightarrow$ Time Limit Exceeded (TLE).

2. **Approach 2 — Two Pointers / Greedy Inward Shrinking (Optimal & Implemented):**
   - Start with maximum width: `left = 0`, `right = height.size() - 1`.
   - Maintain `maxWater = 0`.
   - In each step:
     - Compute `width = right - left`.
     - Compute `h = min(height[left], height[right])`.
     - Update `maxWater = max(maxWater, width * h)`.
     - Shift the pointer pointing to the shorter vertical line inward (`++left` if `height[left] < height[right]`, else `--right`).
   - *Verdict:* Optimal $O(N)$ time and strictly $O(1)$ space. Single pass, cache-friendly, eliminates thousands of sub-optimal pairs at each decision step.

---

## 3. Complexity Analysis

- **Time Complexity:** $O(N)$
  - `left` and `right` start at the extremes ($0$ and $N - 1$) and move towards each other by $1$ unit per iteration.
  - The while loop executes exactly $N - 1$ times before the pointers meet.
- **Space Complexity:** $O(1)$
  - Only scalar integers (`left`, `right`, `maxWater`, `width`, `h`) are stored on the stack. No heap allocation or extra memory used.

---

## 4. Edge Cases & Gotchas

- [x] **Equal heights (`height[left] == height[right]`):** Either pointer can be moved without missing the optimal solution. In the implementation, moving `--right` (the `else` branch) is completely safe.
- [x] **Strictly ascending or strictly descending arrays (e.g. `[1, 2, 3, 4, 5]` or `[5, 4, 3, 2, 1]`):** The shorter boundary is sequentially discarded until the highest bars are compared.
- [x] **Minimum input size ($N = 2$):** Executes the loop once, correctly evaluates the single available container, and terminates.
- [x] **Tall narrow container vs. short wide container (e.g. `[1, 1000, 1000, 1]`):** The wide outer container (`1 * 3 = 3`) is replaced by the tall inner container (`1000 * 1 = 1000`) as soon as the outer pointers step inward.

---

## 5. Clean Code (Optimal Solution: Two Pointers)

```cpp
class Solution {
public:
    int maxArea(vector<int>& height) {
        int left = 0;
        int right = static_cast<int>(height.size()) - 1;
        int maxWater = 0;

        while (left < right) {
            int width = right - left;
            int h = min(height[left], height[right]);
            maxWater = max(maxWater, width * h);

            // Bottleneck is the shorter side: always move the shorter pointer inward
            if (height[left] < height[right]) {
                ++left;
            } else {
                --right;
            }
        }

        return maxWater;
    }
};
```

---

## 6. Review & Takeaways

### Visualizing the Greedy Decision Rule

Given `height = [1, 8, 6, 2, 5, 4, 8, 3, 7]`:

```text
Step 1:
 left                                      right
  ↓                                          ↓
[ 1,   8,   6,   2,   5,   4,   8,   3,   7 ]
width = 8 - 0 = 8
h = min(1, 7) = 1
area = 8 * 1 = 8 -> maxWater = 8
Since height[left] (1) < height[right] (7):
-> Bar '1' has yielded its maximum possible area (width 8 is the maximum possible).
-> Any inner bar paired with bar '1' has width < 8 and height <= 1 -> area strictly < 8.
-> We must discard and advance left: ++left

Step 2:
      left                                 right
        ↓                                    ↓
[ 1,   8,   6,   2,   5,   4,   8,   3,   7 ]
width = 8 - 1 = 7
h = min(8, 7) = 7
area = 7 * 7 = 49 -> maxWater = 49
Since height[left] (8) > height[right] (7):
-> Bar '7' is the limiting bottleneck -> Decrement right: --right

... (continue converging toward center) ...
Final maxWater = 49 (formed by bar 8 at index 1 and bar 7 at index 8).
```

---

### The Two Pointers Elimination Invariant

```text
Container capacity is bounded by the shorter wall
                  ↓
       Width monotonically shrinks (N-1 -> 1)
                  ↓
   To increase area, minimum height MUST increase
                  ↓
Retaining shorter wall guarantees smaller area (width shrinks, height capped)
                  ↓
Golden Rule: Always advance pointer at the SHORTER wall
```

---

### The Architectural Pattern

```text
Container With Most Water
           ↓
Two Pointers (left = 0, right = n - 1)
           ↓
while left < right:
  ├─ width = right - left
  ├─ h = min(height[left], height[right])
  ├─ maxWater = max(maxWater, width * h)
  └─ height[left] < height[right] ? ++left : --right
```

* **Next Review Date:** Low priority (benchmark greedy two-pointer reduction pattern mastered).
* **Key Takeaway:** When searching for an optimal 2-element span where capacity is bounded by the minimum element, start at maximum width and greedily discard the bottleneck boundary.
