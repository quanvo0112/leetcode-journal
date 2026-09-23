# 0167. Two Sum II - Input Array Is Sorted

- **Problem Link:** https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/
- **Difficulty:** `Medium`
- **NeetCode Category:** `Two Pointers`
- **LeetCode Topics:** `Array` / `Two Pointers` / `Binary Search`
- **Core Pattern:** `Converging Two Pointers on Sorted Array`
- **Last Practiced:** 2026-09-19
- **Proficiency Level:** 
  - [x] Level 1: Solved smoothly (< 20 mins, optimal)
  - [ ] Level 2: Struggled / Non-optimal / Edge-case bugs
  - [ ] Level 3: Needed editorial or hints

---

## 1. Pattern Recognition & Triggers

- **Clues in prompt:** *"array is already sorted in non-decreasing order"*, *"your solution must use only constant extra space"*, *"1-indexed"*.
- **Core intuition:** Unlike the original Two Sum (LeetCode 1) where the input is unsorted and requires an $O(N)$ hash map, here the array is **already sorted**.
  - Sorted order provides strict **monotonicity**: placing pointers at opposite boundaries (`left = 0`, `right = n - 1`) enables predictable sum adjustments.
  - If `numbers[left] + numbers[right] < target`, the sum is too small; because `numbers[right]` is already the largest available partner for `numbers[left]`, no other element can pair with `numbers[left]` to reach `target`. Hence, `numbers[left]` is eliminated safely by advancing `++left`.
  - Conversely, if `numbers[left] + numbers[right] > target`, the sum is too large; because `numbers[left]` is the smallest available partner for `numbers[right]`, no other element can pair with `numbers[right]` to reach `target`. Hence, `numbers[right]` is eliminated by decrementing `--right`.

---

## 2. Approach & Trade-offs

1. **Approach 1 — Hash Map ($O(N)$ Time, $O(N)$ Space):**
   - Store visited values in an `unordered_map<int, int>` as in Two Sum I.
   - *Verdict:* Violates the problem's strict constraint of using $O(1)$ extra memory, completely ignoring the sorted property.

2. **Approach 2 — Binary Search ($O(N \log N)$ Time, $O(1)$ Space):**
   - For each element `numbers[i]`, use binary search (`std::binary_search` or `std::lower_bound`) to find `target - numbers[i]` in the remainder of the array.
   - *Verdict:* Meets the $O(1)$ space constraint, but $O(N \log N)$ time is sub-optimal compared to a linear two-pointer scan.

3. **Approach 3 — Two Pointers (Optimal & Implemented):**
   - Initialize `left = 0` and `right = numbers.size() - 1`.
   - Compute `sum = numbers[left] + numbers[right]`.
   - If `sum == target`: return `{left + 1, right + 1}` (accounting for 1-based indexing).
   - If `sum < target`: `++left;` (need a larger sum).
   - If `sum > target`: `--right;` (need a smaller sum).
   - *Verdict:* Optimal $O(N)$ time and strictly $O(1)$ space. Zero dynamic allocations, single pass, highly cache-friendly.

---

## 3. Complexity Analysis

- **Time Complexity:** $O(N)$
  - With each comparison, either `left` is incremented or `right` is decremented.
  - The pointers converge towards each other, guaranteeing termination in at most $N - 1$ steps.
- **Space Complexity:** $O(1)$
  - Only two scalar pointer indices (`left`, `right`) and a scalar integer `sum` stored on the stack. No auxiliary memory allocated.

---

## 4. Edge Cases & Gotchas

- [x] **1-indexed output:** The problem explicitly demands 1-indexed positions. Returning `{left, right}` results in Wrong Answer; must return `{left + 1, right + 1}`.
- [x] **Negative numbers and zeroes (e.g. `numbers = [-3, -1, 0, 4]`, `target = -4`):** Handled transparently by two's complement integer arithmetic without special branching.
- [x] **Minimum sized input ($N = 2$):** Pointers initialize to `left = 0` and `right = 1`, evaluating and matching on the very first iteration.
- [x] **Duplicates in array (e.g. `numbers = [1, 2, 2, 4]`, `target = 4`):** Handled correctly as the pointers converge to index 1 and 2, returning `{2, 3}`.

---

## 5. Clean Code (Optimal Solution: Two Pointers)

```cpp
class Solution {
public:
    vector<int> twoSum(vector<int>& numbers, int target) {
        int left = 0;
        int right = static_cast<int>(numbers.size()) - 1;

        while (left < right) {
            int sum = numbers[left] + numbers[right];

            if (sum == target) {
                return {left + 1, right + 1};
            }

            if (sum < target) {
                ++left;
            } else {
                --right;
            }
        }

        return {};
    }
};
```

---

## 6. Review & Takeaways

### Visualizing Two Pointers Convergence

Given `numbers = [2, 7, 11, 15]`, `target = 9`:

```text
Step 1:
 left                      right
  ↓                          ↓
[ 2,    7,     11,          15 ]
sum = 2 + 15 = 17 > 9 (too large)
-> Since array is sorted ascending, 15 paired with the smallest element (2) already exceeds 9,
   so 15 cannot pair with any other element to reach 9.
-> Eliminate 15: --right

Step 2:
 left               right
  ↓                   ↓
[ 2,    7,     11,   15 ]
sum = 2 + 11 = 13 > 9 (still too large)
-> Similarly, eliminate 11: --right

Step 3:
 left   right
  ↓       ↓
[ 2,      7,   11,   15 ]
sum = 2 + 7 = 9 == target -> MATCH!
-> Return 1-indexed: {left + 1, right + 1} = {1, 2}
```

---

### Core Pointer Movement Invariant

```text
sum < target  →  need larger sum   →  left++
sum > target  →  need smaller sum   →  right--
sum == target →  match found      →  return {left + 1, right + 1}
```

```text
       sum too small (sum < target)
            left  →
     [  .   .   .   .   .   .   .  ]
                        ←  right
       sum too large (sum > target)
```

---

### The Architectural Pattern

```text
Two Sum II (Sorted Array)
           ↓
Two Pointers (left = 0, right = n - 1)
           ↓
Loop while left < right:
  ├─ sum < target  → ++left
  ├─ sum > target  → --right
  └─ sum == target → return {left + 1, right + 1}
```

* **Next Review Date:** Low priority (benchmark sorted two-pointer pattern mastered).
* **Key Takeaway:** When searching for a target pair in an array that is **already sorted**, avoid hash maps or nested loops; two opposing pointers provide the optimal $O(N)$ time and $O(1)$ space solution by exploiting monotonic bounds.
