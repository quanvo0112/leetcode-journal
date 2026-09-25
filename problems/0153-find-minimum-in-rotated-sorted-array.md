# 0153. Find Minimum in Rotated Sorted Array

- **Problem Link:** https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/
- **Difficulty:** `Medium`
- **NeetCode Category:** `Binary Search`
- **LeetCode Topics:** `Array` / `Binary Search`
- **Core Pattern:** `Binary Search on Rotated Array (Boundary Invariant via nums[mid] vs nums[right])`
- **Last Practiced:** 2026-09-25
- **Proficiency Level:**
  - [x] Level 1: Solved smoothly (< 20 mins, optimal)
  - [ ] Level 2: Struggled / Non-optimal / Edge-case bugs
  - [ ] Level 3: Needed editorial or hints

---

## 1. Pattern Recognition & Triggers

- **Clues in prompt:**
  - An array of length `n` sorted in ascending order is rotated between `1` and `n` times.
  - All integers in `nums` are **unique**.
  - You must write an algorithm that runs in $O(\log n)$ time.
- **Core intuition:**
  - A rotated sorted array is partitioned into two distinct sorted segments:
    $$\underbrace{[4, 5, 6, 7]}_{\text{Left Sorted Portion}} \quad \underbrace{[0, 1, 2]}_{\text{Right Sorted Portion}}$$
  - Notice the key structural invariant:
    - Every element in the **Left Sorted Portion** is strictly greater than every element in the **Right Sorted Portion**.
    - The **inflection point** (the minimum element, e.g. `0`) is the very first element of the Right Sorted Portion.
  - To determine which portion contains the inflection point, we compare `nums[mid]` against the rightmost boundary `nums[right]`:
    - **Case 1: `nums[mid] > nums[right]`**
      - `nums[mid]` is strictly larger than the right end, which means `mid` must reside inside the **Left Sorted Portion**.
      - The minimum element must lie strictly to the right of `mid`:
        $$\text{left} = \text{mid} + 1$$
    - **Case 2: `nums[mid] <= nums[right]`**
      - The subarray from `mid` to `right` is monotonically increasing.
      - Therefore, the minimum element cannot lie strictly to the right of `mid`. It must either be `mid` itself or located to the left of `mid`:
        $$\text{right} = \text{mid}$$

---

## 2. Approach & Trade-offs

1. **Approach 1 — Linear Scan ($O(N)$ Time, $O(1)$ Space):**
   - Scan the array to find the minimum element in $O(N)$ time.
   - *Verdict:* Violates the strict $O(\log N)$ requirement; completely ignores the underlying sorted structure.

2. **Approach 2 — Binary Search with `nums[left]` Comparison ($O(\log N)$ Time, $O(1)$ Space):**
   - Compare `nums[mid]` with `nums[left]`.
   - *Verdict:* Requires explicit handling when the array is already fully sorted (`nums[left] < nums[right]`), introducing redundant branching.

3. **Approach 3 — Binary Search with `nums[mid]` vs `nums[right]` (Chosen Optimal Solution):**
   - Initialize `left = 0`, `right = nums.size() - 1`.
   - While `left < right`:
     - `mid = left + (right - left) / 2`.
     - If `nums[mid] > nums[right]`: `left = mid + 1`.
     - Else: `right = mid`.
   - Loop converges when `left == right`, pointing directly to the minimum element.
   - *Verdict:* Optimal $O(\log N)$ Time, $O(1)$ Space. Seamlessly handles both rotated and non-rotated arrays without special branch conditions.

---

## 3. Complexity Analysis

- **Time Complexity:** $O(\log N)$
  - With each iteration, the search interval $[left, right]$ is halved.
  - The loop terminates in at most $\lfloor \log_2 N \rfloor + 1$ iterations.
- **Space Complexity:** $O(1)$
  - Only scalar indices (`left`, `right`, `mid`) are stored on the call stack; no auxiliary data structures.

---

## 4. Edge Cases & Gotchas

- [x] **Unrotated Array or Rotated by $N$ times (e.g. `[11, 13, 15, 17]`):**
  - `nums[mid] < nums[right]` holds true in every step.
  - `right` repeatedly contracts to `mid` until `left == right == 0`, correctly returning `nums[0] = 11`. No special casing required.
- [x] **Single Element Array ($N = 1$, e.g. `[5]`):**
  - `left = 0, right = 0`. The condition `left < right` is immediately false, returning `nums[0] = 5` correctly.
- [x] **Two-Element Array (e.g. `[2, 1]` or `[1, 2]`):**
  - For `[2, 1]`: `mid = 0`, `nums[0] > nums[1]` $\implies$ `left = 1`. Returns `nums[1] = 1`.
  - For `[1, 2]`: `mid = 0`, `nums[0] <= nums[1]` $\implies$ `right = 0`. Returns `nums[0] = 1`.
- [x] **Why `right = mid` instead of `right = mid - 1`?**
  - When `nums[mid] <= nums[right]`, `nums[mid]` itself might be the minimum element (e.g., `[4, 5, 0, 1, 2]` with `mid = 2`, `nums[2] = 0`). Discarding `mid` with `mid - 1` would eliminate the correct answer.
- [x] **Why `while (left < right)`?**
  - The invariant guarantees that the minimum element is always within $[left, right]$. When `left == right`, the search space has collapsed to exactly one candidate. Continuing with `<=` could cause an infinite loop because `right = mid` does not shrink the range when `left == right`.

---

## 5. Clean Code (Optimal Solution: Binary Search mid vs right)

```cpp
#include <vector>

using namespace std;

class Solution {
public:
    int findMin(vector<int>& nums) {
        int left = 0;
        int right = static_cast<int>(nums.size()) - 1;

        // Invariant: the minimum element always lies within [left, right]
        while (left < right) {
            int mid = left + (right - left) / 2;

            if (nums[mid] > nums[right]) {
                // mid is in the left sorted portion; minimum is strictly to the right
                left = mid + 1;
            } else {
                // mid is in the right sorted portion; minimum is at mid or to its left
                right = mid;
            }
        }

        return nums[left]; // Converged at the unique minimum element
    }
};
```

---

## 6. Review & Takeaways

### Step-by-Step Dry Run

Given `nums = [3, 4, 5, 1, 2]`:

```text
Initial state:
  left = 0, right = 4
  nums = [3,  4,  5,  1,  2]
          ↑       ↑       ↑
         left    mid    right

Iteration 1:
  mid = 0 + (4 - 0) / 2 = 2
  nums[mid] = 5, nums[right] = 2
  Comparison: 5 > 2 (nums[mid] > nums[right])
  -> 5 belongs to the left sorted portion.
  -> Minimum lies strictly to the right.
  -> left = mid + 1 = 3
  Active range: [3, 4]

Iteration 2:
  left = 3, right = 4
  nums = [3, 4, 5,  1,  2]
                    ↑   ↑
                   mid right
                   left
  mid = 3 + (4 - 3) / 2 = 3
  nums[mid] = 1, nums[right] = 2
  Comparison: 1 <= 2 (nums[mid] <= nums[right])
  -> 1 belongs to the right sorted portion.
  -> Minimum could be mid itself.
  -> right = mid = 3
  Active range: [3, 3]

Loop terminates: left == right == 3.
Return nums[3] = 1.
```

---

### The Architectural Pattern

```text
               Rotated Sorted Array [left ... right]
                                 ↓
                        while left < right:
                                 ↓
                     mid = left + (right - left) / 2
                                 ↓
                      nums[mid] > nums[right] ?
                             /        \
                       YES  /          \  NO
                           ↓            ↓
                    left = mid + 1   right = mid
                 (Inflection is on  (Inflection is at
                   the right side)   mid or on the left)
                           \            /
                            \          /
                             └────┬───┘
                                  ↓
                        return nums[left]
```

* **Next Review Date:** Low priority (benchmark rotated array inflection point binary search pattern mastered).
* **Key Takeaway:** In any rotated sorted array with unique elements, compare `nums[mid]` against `nums[right]`. If `nums[mid] > nums[right]`, the pivot is strictly to the right (`left = mid + 1`); otherwise, it is at or to the left of `mid` (`right = mid`).
