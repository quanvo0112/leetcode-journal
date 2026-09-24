# 0042. Trapping Rain Water

- **Problem Link:** https://leetcode.com/problems/trapping-rain-water/
- **Difficulty:** `Hard`
- **NeetCode Category:** `Two Pointers`
- **LeetCode Topics:** `Array` / `Two Pointers` / `Dynamic Programming` / `Stack` / `Monotonic Stack`
- **Core Pattern:** `Two Pointers with Running leftMax & rightMax`
- **Last Practiced:** 2026-09-20
- **Proficiency Level:**
  - [x] Level 1: Solved smoothly (< 20 mins, optimal)
  - [ ] Level 2: Struggled / Non-optimal / Edge-case bugs
  - [ ] Level 3: Needed editorial or hints

---

## 1. Pattern Recognition & Triggers

- **Clues in prompt:** *"elevation map where the width of each bar is 1"*, *"compute how much water it can trap after raining"*.
- **Core intuition:**
  - The amount of water trapped directly above any vertical bar at index $i$ depends strictly on the lowest of the two highest surrounding walls:
    $$\text{water}[i] = \max(0, \min(\text{maxLeft}[i], \text{maxRight}[i]) - height[i])$$
  - Computing `maxLeft[i]` and `maxRight[i]` using prefix and suffix arrays requires $O(N)$ auxiliary memory.
  - **The Two Pointers Insight:** We do not need to know the *exact* maximum on both sides simultaneously. We only need to know **which side is the bottleneck**.
    - If `height[left] <= height[right]`: We know with mathematical certainty that there is already a boundary to the right that is at least as tall as `height[left]`. Thus, the right side can never be the limiting factor for `left`. The water trapped at `left` is entirely governed by `leftMax`.
    - If `height[right] < height[left]`: Symmetrically, there is a boundary to the left at least as tall as `height[right]`. The water trapped at `right` is strictly governed by `rightMax`.
  - **Core Rule:** Always advance and process the side with the smaller boundary height (the bottleneck).

---

## 2. Approach & Trade-offs

1. **Approach 1 — Brute Force ($O(N^2)$ Time, $O(1)$ Space):**
   - For every index $i$, scan left to find the maximum height, and scan right to find the maximum height.
   - *Verdict:* $O(N^2)$ time triggers Time Limit Exceeded (TLE) for $N = 2 \times 10^4$.

2. **Approach 2 — Prefix & Suffix Max Arrays ($O(N)$ Time, $O(N)$ Space):**
   - Precompute `prefixMax[i]` from left-to-right and `suffixMax[i]` from right-to-left.
   - Compute $\sum \min(prefixMax[i], suffixMax[i]) - height[i]$.
   - *Verdict:* $O(N)$ time, but requires allocating two $O(N)$ auxiliary arrays.

3. **Approach 3 — Monotonic Stack ($O(N)$ Time, $O(N)$ Space):**
   - Maintain a decreasing monotonic stack of indices to calculate trapped water layer-by-layer horizontally.
   - *Verdict:* $O(N)$ time, but harder to implement and requires $O(N)$ stack memory.

4. **Approach 4 — Two Pointers with `leftMax` and `rightMax` (Optimal & Implemented):**
   - Place two pointers at opposite ends: `left = 0`, `right = n - 1`.
   - Track running variables `leftMax = 0` and `rightMax = 0`.
   - While `left < right`:
     - If `height[left] <= height[right]`:
       - `leftMax = max(leftMax, height[left]);`
       - `water += leftMax - height[left];`
       - `++left;`
     - Else (`height[right] < height[left]`):
       - `rightMax = max(rightMax, height[right]);`
       - `water += rightMax - height[right];`
       - `--right;`
   - *Verdict:* Strictly optimal $O(N)$ time and $O(1)$ auxiliary space. Single pass, cache-friendly, zero heap allocation.

---

## 3. Complexity Analysis

- **Time Complexity:** $O(N)$
  - Each element in the `height` array is visited and processed exactly once as the two pointers converge inward from opposite ends.
  - Terminates in at most $N - 1$ steps.
- **Space Complexity:** $O(1)$
  - Only scalar integers (`left`, `right`, `leftMax`, `rightMax`, `water`) are maintained on the stack. No arrays or stacks allocated.

---

## 4. Edge Cases & Gotchas

- [x] **Order of Operations (Crucial Gotcha):**
  You must update `leftMax` *before* computing the water difference:
  ```cpp
  leftMax = max(leftMax, height[left]);
  water += leftMax - height[left];
  ++left;
  ```
  If `height[left]` is the new maximum, `leftMax - height[left] = 0` (no water trapped on top of a peak). If it is lower than `leftMax`, water is trapped and added immediately.
- [x] **Small input ($N \le 2$):** A container requires at least two walls with a gap between them to hold water. If $N < 3$, the loop terminates without trapping water, returning `0`.
- [x] **Strictly ascending or descending elevations (e.g. `[1, 2, 3, 4]` or `[5, 4, 3, 1]`):** Water difference is always `0` at each step; returns `0`.
- [x] **All equal elevations (e.g. `[3, 3, 3, 3]`):** Flat surface cannot trap water; correctly returns `0`.

---

## 5. Clean Code (Optimal Solution: Two Pointers)

```cpp
class Solution {
public:
    int trap(vector<int>& height) {
        int left = 0;
        int right = static_cast<int>(height.size()) - 1;

        int leftMax = 0;
        int rightMax = 0;

        int water = 0;

        while (left < right) {
            if (height[left] <= height[right]) {
                leftMax = max(leftMax, height[left]);
                water += leftMax - height[left];
                ++left;
            } else {
                rightMax = max(rightMax, height[right]);
                water += rightMax - height[right];
                --right;
            }
        }

        return water;
    }
};
```

---

## 6. Review & Takeaways

### Visualizing Rain Water Trapping

Given `height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]`:

```text
3 |                      █
2 |          █  ~  ~  ~  █  █  ~  █
1 |    █  ~  █  █  ~  █  █  █  █  █  █
0 | █  █  █  █  █  █  █  █  █  █  █  █
  +------------------------------------
    0  1  2  3  4  5  6  7  8  9 10 11
```
*(Legend: `█` = elevation bar, `~` = trapped rain water. Total units = 6)*

---

### Step-by-Step Execution Trace

```text
Initial: left = 0 (h=0), right = 11 (h=1), leftMax = 0, rightMax = 0, water = 0

1. height[0] (0) <= height[11] (1):
   leftMax = max(0, 0) = 0 -> water += 0 - 0 = 0 -> ++left (left = 1)
2. height[1] (1) <= height[11] (1):
   leftMax = max(0, 1) = 1 -> water += 1 - 1 = 0 -> ++left (left = 2)
3. height[2] (0) <= height[11] (1):
   leftMax = max(1, 0) = 1 -> water += 1 - 0 = 1 -> ++left (left = 3) [WATER +1]
4. height[3] (2) > height[11] (1):
   rightMax = max(0, 1) = 1 -> water += 1 - 1 = 0 -> --right (right = 10)
5. height[3] (2) <= height[10] (2):
   leftMax = max(1, 2) = 2 -> water += 2 - 2 = 0 -> ++left (left = 4)
6. height[4] (1) <= height[10] (2):
   leftMax = max(2, 1) = 2 -> water += 2 - 1 = 1 -> ++left (left = 5) [WATER +1]
7. height[5] (0) <= height[10] (2):
   leftMax = max(2, 0) = 2 -> water += 2 - 0 = 2 -> ++left (left = 6) [WATER +2]
8. height[6] (1) <= height[10] (2):
   leftMax = max(2, 1) = 2 -> water += 2 - 1 = 1 -> ++left (left = 7) [WATER +1]
9. height[7] (3) > height[10] (2):
   rightMax = max(1, 2) = 2 -> water += 2 - 2 = 0 -> --right (right = 9)
10. height[7] (3) > height[9] (1):
   rightMax = max(2, 1) = 2 -> water += 2 - 1 = 1 -> --right (right = 8) [WATER +1]
11. height[7] (3) > height[8] (2):
   rightMax = max(2, 2) = 2 -> water += 2 - 2 = 0 -> --right (right = 7)

left meets right at index 7 (highest peak). Loop terminates.
Total Trapped Water = 1 + 1 + 2 + 1 + 1 = 6.
```

---

### The Two Pointers Master Rule

```text
Trapping Rain Water
        ↓
Two Pointers (left = 0, right = n - 1)
        ↓
leftMax / rightMax tracking
        ↓
height[left] <= height[right] ?
  ├─ TRUE  → Process left:  update leftMax,  water += leftMax - height[left],   ++left
  └─ FALSE → Process right: update rightMax, water += rightMax - height[right], --right
```

> **Always process the bottleneck (smaller side) first.**

---

### NeetCode 150 Pattern Progress Checklist

```text
[Topic 1: Arrays & Hashing - 9/9 COMPLETED]
  1. Two Sum                         -> Hash Map
  2. Valid Anagram                   -> Frequency Counting
  3. Contains Duplicate              -> Hash Set
  4. Group Anagrams                  -> Frequency Signature + Hash Map
  5. Top K Frequent Elements         -> Bucket Sort
  6. Encode & Decode Strings         -> Length-Prefix Delimitation
  7. Product of Array Except Self    -> Prefix + Suffix Direct Accumulation
  8. Valid Sudoku                    -> 9-bit Bitmask per Row/Col/Box
  9. Longest Consecutive Sequence    -> Hash Set + Sequence Start

[Topic 2: Two Pointers - 5/5 COMPLETED]
 10. Valid Palindrome                -> Two Pointers (Safe <cctype> In-Place)
 11. Two Sum II - Sorted Array       -> Two Pointers (Monotonic Convergence)
 12. 3Sum                            -> Sort + Fix i + Two Sum II + Duplicate Skip
 13. Container With Most Water       -> Two Pointers + Move Shorter Side
 14. Trapping Rain Water             -> Two Pointers + leftMax/rightMax Bottleneck
```

* **Next Review Date:** Low priority (benchmark dynamic elevation two-pointer reduction mastered).
* **Key Takeaway:** By determining which boundary acts as the strict bottleneck (`height[left] <= height[right]`), we eliminate the need for prefix/suffix arrays, computing trapped water column-by-column in optimal $O(N)$ time and $O(1)$ space.
