# 0704. Binary Search

- **Problem Link:** https://leetcode.com/problems/binary-search/
- **Difficulty:** `Easy`
- **NeetCode Category:** `Binary Search`
- **LeetCode Topics:** `Array` / `Binary Search`
- **Core Pattern:** `Iterative Binary Search on Closed Interval [left, right]`
- **Last Practiced:** 2026-09-24
- **Proficiency Level:**
  - [x] Level 1: Solved smoothly (< 20 mins, optimal)
  - [ ] Level 2: Struggled / Non-optimal / Edge-case bugs
  - [ ] Level 3: Needed editorial or hints

---

## 1. Pattern Recognition & Triggers

- **Clues in prompt:**
  - *"Given an array of integers `nums` which is sorted in ascending order..."*
  - *"You must write an algorithm with $O(\log n)$ runtime complexity."*
- **Core intuition:**
  - The input array is **strictly sorted in ascending order**.
  - Sorted order provides strict **monotonicity**: checking the midpoint element `nums[mid]` allows us to eliminate half of the remaining search space in $O(1)$ time:
    - If `nums[mid] == target`: Found immediately; return index `mid`.
    - If `nums[mid] < target`: Because the array is sorted, every element at or to the left of `mid` is strictly smaller than `target`. The target can only exist in the right subarray $\implies \text{left} = \text{mid} + 1$.
    - If `nums[mid] > target`: Symmetrically, every element at or to the right of `mid` is strictly greater than `target`. The target can only exist in the left subarray $\implies \text{right} = \text{mid} - 1$.
  - Repeating this halving process reduces an $N$-element search space to $\le 0$ elements in $\lceil \log_2 N \rceil$ comparisons.

---

## 2. Approach & Trade-offs

1. **Approach 1 — Linear Scan ($O(N)$ Time, $O(1)$ Space):**
   - Iterate through the array from index $0$ to $N - 1$.
   - *Verdict:* Violates the strict $O(\log N)$ requirement; completely ignores the sorted invariant.

2. **Approach 2 — Recursive Binary Search ($O(\log N)$ Time, $O(\log N)$ Space):**
   - Implement binary search using a helper function `search(nums, target, left, right)` calling itself with halved bounds.
   - *Verdict:* Achieving $O(\log N)$ time, but consumes $O(\log N)$ auxiliary space on the call stack due to recursion frames. Sub-optimal compared to iterative search.

3. **Approach 3 — Iterative Closed Interval Search (Chosen Optimal Solution):**
   - Initialize two boundary pointers: `left = 0` and `right = nums.size() - 1`.
   - Maintain the search range as a **closed interval** `[left, right]`.
   - Loop condition `while (left <= right)`:
     - Compute safe midpoint: `mid = left + (right - left) / 2`.
     - Branch into `mid + 1` or `mid - 1` based on comparison with `target`.
   - *Verdict:* Optimal $O(\log N)$ Time, strictly $O(1)$ Auxiliary Space. Standard, robust, and zero stack memory overhead.

---

## 3. Complexity Analysis

- **Time Complexity:** $O(\log N)$
  - With each step of the `while` loop, the length of the search space $[left, right]$ is halved:
    $$\frac{N}{2} \rightarrow \frac{N}{4} \rightarrow \frac{N}{8} \dots \rightarrow 1$$
  - The maximum number of iterations is $\lfloor \log_2 N \rfloor + 1$.
- **Space Complexity:** $O(1)$
  - Only three scalar integer variables (`left`, `right`, `mid`) are maintained on the stack. No heap allocation, no recursion frames.

---

## 4. Edge Cases & Gotchas

- [x] **Integer Overflow in Midpoint Calculation:**
  - Writing `mid = (left + right) / 2` risks 32-bit signed integer overflow if `left + right > INT_MAX` ($2^{31} - 1$).
  - Writing `mid = left + (right - left) / 2` subtracts before adding, ensuring the intermediate calculation never exceeds `right`, preventing overflow entirely.
- [x] **Why `while (left <= right)` instead of `while (left < right)`?**
  - Our search boundary is defined as the **closed interval** `[left, right]`, meaning both `left` and `right` are valid candidates.
  - If the array has a single element (e.g., `nums = [5], target = 5`), `left = 0` and `right = 0`. With `<` the loop would terminate immediately without checking `nums[0]`. The `<=` condition ensures single-element intervals are always inspected.
- [x] **Target at Array Boundaries (First or Last Element):**
  - Target at index $0$: `right` repeatedly decrements until `mid = 0`, matching correctly.
  - Target at index $N - 1$: `left` repeatedly increments until `mid = N - 1`, matching correctly.
- [x] **Target Not in Array:**
  - `left` eventually overtakes `right` (`left > right`), the search space becomes empty, the loop terminates, and `-1` is returned.

---

## 5. Clean Code (Optimal Solution: Iterative Binary Search)

```cpp
#include <vector>

using namespace std;

class Solution {
public:
    int search(vector<int>& nums, int target) {
        int left = 0;
        int right = static_cast<int>(nums.size()) - 1;

        // Search space is the closed interval [left, right]
        while (left <= right) {
            // Safe midpoint calculation avoiding integer overflow
            int mid = left + (right - left) / 2;

            if (nums[mid] == target) {
                return mid;
            }

            if (nums[mid] < target) {
                // Target must be strictly in the right half
                left = mid + 1;
            } else {
                // Target must be strictly in the left half
                right = mid - 1;
            }
        }

        return -1; // Target not found
    }
};
```

---

## 6. Review & Takeaways

### Step-by-Step Dry Run

Given `nums = [-1, 0, 3, 5, 9, 12]`, `target = 9`:

```text
Initial state:
  left = 0, right = 5, search interval: [0, 5]

Iteration 1:
  mid = 0 + (5 - 0) / 2 = 2
  nums[mid] = nums[2] = 3
  Comparison: 3 < 9 (nums[mid] < target)
  -> Target lies strictly to the right.
  -> left = mid + 1 = 3

Iteration 2:
  left = 3, right = 5, search interval: [3, 5]
  Active subarray: [5, 9, 12]
                    ↑  ↑   ↑
                   left mid right
  mid = 3 + (5 - 3) / 2 = 4
  nums[mid] = nums[4] = 9
  Comparison: 9 == 9 (nums[mid] == target)
  -> Match found!
  -> Return 4.
```

---

### The Architectural Pattern

```text
                     Sorted Array [0 ... n-1]
                                ↓
                      left = 0, right = n - 1
                                ↓
                      while left <= right:
                                ↓
                  mid = left + (right - left) / 2
                                ↓
                    nums[mid] vs target
                   /         |         \
                  /          |          \
                 <           ==          >
                ↓            ↓            ↓
          left = mid + 1  return mid   right = mid - 1
```

* **Next Review Date:** Low priority (benchmark logarithmic binary search pattern mastered).
* **Key Takeaway:** For any monotonic search space, maintain consistent interval semantics (`[left, right]` with `<=` and `mid ± 1`) and compute `mid = left + (right - left) / 2` to eliminate boundary errors and integer overflows.
