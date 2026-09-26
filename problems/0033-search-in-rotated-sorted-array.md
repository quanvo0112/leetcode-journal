# 0033. Search in Rotated Sorted Array

- **Problem Link:** https://leetcode.com/problems/search-in-rotated-sorted-array/
- **Difficulty:** `Medium`
- **NeetCode Category:** `Binary Search`
- **LeetCode Topics:** `Array` / `Binary Search`
- **Core Pattern:** `Modified Binary Search on Rotated Array (Identify Sorted Half & Check Boundary Invariant)`
- **Last Practiced:** 2026-09-26
- **Proficiency Level:**
  - [x] Level 1: Solved smoothly (< 20 mins, optimal)
  - [ ] Level 2: Struggled / Non-optimal / Edge-case bugs
  - [ ] Level 3: Needed editorial or hints

---

## 1. Pattern Recognition & Triggers

- **Clues in prompt:**
  - An integer array `nums` sorted in ascending order with **all unique values** is rotated at an unknown pivot.
  - Given a `target`, return its index if found, or `-1` if not present.
  - You must achieve an $O(\log n)$ runtime complexity.
- **Core intuition:**
  - Unlike standard binary search where the entire array is sorted, here the rotation splits the array into two offset segments.
  - **The Golden Invariant:** Any midpoint index `mid` divides the rotated array into two halves, and **at least one of the two halves is guaranteed to be strictly sorted**.
  - Instead of searching for the rotation pivot first, we can resolve the problem in a **single pass**:
    1. Check if `nums[mid] == target`. If so, return `mid`.
    2. Determine which half is monotonically sorted:
       - If `nums[left] <= nums[mid]`: The **left half** $[left \dots mid]$ is sorted.
       - Otherwise: The **right half** $[mid \dots right]$ is sorted.
    3. Check whether `target` falls within the boundary values of the sorted half:
       - If yes: Confine search to that sorted half.
       - If no: Target must reside in the opposite (unsorted/rotated) half.

---

## 2. Approach & Trade-offs

1. **Approach 1 — Linear Scan ($O(N)$ Time, $O(1)$ Space):**
   - Iterate through the array to check `nums[i] == target`.
   - *Verdict:* Violates the strict $O(\log N)$ requirement; fails to exploit the sorted property.

2. **Approach 2 — Two-Pass Binary Search (Find Pivot First, Then Binary Search) ($O(\log N)$ Time, $O(1)$ Space):**
   - Phase 1: Use binary search to find the minimum element / pivot index (as in LeetCode 153).
   - Phase 2: Perform standard binary search on either the left or right segment.
   - *Verdict:* Valid $O(\log N)$, but requires two separate search procedures, extra boundary logic, and is more verbose than a single pass.

3. **Approach 3 — Single-Pass Modified Binary Search (Chosen Optimal Solution):**
   - Maintain search boundaries `left = 0`, `right = nums.size() - 1`.
   - While `left <= right`:
     - Compute midpoint: `mid = left + (right - left) / 2`.
     - If `nums[mid] == target`: return `mid`.
     - **Branch 1: Left half is sorted (`nums[left] <= nums[mid]`):**
       - Check if `target` is in range: `nums[left] <= target && target < nums[mid]`.
       - If true: `right = mid - 1`.
       - If false: `left = mid + 1`.
     - **Branch 2: Right half is sorted (`nums[left] > nums[mid]`):**
       - Check if `target` is in range: `nums[mid] < target && target <= nums[right]`.
       - If true: `left = mid + 1`.
       - If false: `right = mid - 1`.
   - Return `-1` if loop terminates without finding `target`.
   - *Verdict:* Optimal $O(\log N)$ Time, $O(1)$ Space. Single clean loop, no redundant pivot searches.

---

## 3. Complexity Analysis

- **Time Complexity:** $O(\log N)$
  - In every iteration, regardless of which half is sorted, the search space is halved based on boundary checks.
  - The maximum number of comparisons is $\lfloor \log_2 N \rfloor + 1$.
- **Space Complexity:** $O(1)$
  - Operates completely in-place using only scalar pointer variables (`left`, `right`, `mid`) on the stack.

---

## 4. Edge Cases & Gotchas

- [x] **Why `nums[left] <= nums[mid]` uses `<=` instead of `<`:**
  - When the search window shrinks to 1 or 2 elements, `left == mid` can occur. Using `<=` guarantees that single-element windows correctly classify as a sorted left half without falling through erroneously.
- [x] **Strict vs Inclusive Bounds for Target:**
  - Because `nums[mid] == target` is already checked at the beginning of the loop, the interval check can strictly exclude `mid`:
    - Left half check: `nums[left] <= target && target < nums[mid]`.
    - Right half check: `nums[mid] < target && target <= nums[right]`.
- [x] **Target at Array Boundaries or Pivot (e.g. `target == nums[0]` or `target == nums[n-1]`):**
  - Inclusive inequality comparisons (`nums[left] <= target` and `target <= nums[right]`) ensure edge values are captured properly.
- [x] **Target Not in Array:**
  - `left` eventually crosses `right` (`left > right`), the loop terminates, and `-1` is returned.
- [x] **Array Not Rotated (Already Sorted):**
  - `nums[left] <= nums[mid]` holds across all iterations; degrades gracefully into standard binary search.

---

## 5. Clean Code (Optimal Solution: Modified Binary Search)

```cpp
#include <vector>

using namespace std;

class Solution {
public:
    int search(vector<int>& nums, int target) {
        int left = 0;
        int right = static_cast<int>(nums.size()) - 1;

        while (left <= right) {
            int mid = left + (right - left) / 2;

            if (nums[mid] == target) {
                return mid;
            }

            // Case 1: Left half [left ... mid] is strictly sorted
            if (nums[left] <= nums[mid]) {
                // Target lies within the sorted left half
                if (nums[left] <= target && target < nums[mid]) {
                    right = mid - 1;
                } else {
                    left = mid + 1;
                }
            }
            // Case 2: Right half [mid ... right] is strictly sorted
            else {
                // Target lies within the sorted right half
                if (nums[mid] < target && target <= nums[right]) {
                    left = mid + 1;
                } else {
                    right = mid - 1;
                }
            }
        }

        return -1; // Target not found
    }
};
```

---

## 6. Review & Takeaways

### Step-by-Step Dry Run

Given `nums = [4, 5, 6, 7, 0, 1, 2]`, `target = 0`:

```text
Initial state:
  left = 0, right = 6
  nums = [4,  5,  6,  7,  0,  1,  2]
          ↑           ↑           ↑
         left        mid        right

Iteration 1:
  mid = 0 + (6 - 0) / 2 = 3
  nums[mid] = 7 (7 != target 0)
  Check sorted half:
    nums[left] (4) <= nums[mid] (7) -> TRUE: Left half [4, 5, 6, 7] is sorted!
  Check target in left half:
    nums[left] (4) <= target (0) && target (0) < nums[mid] (7) -> FALSE
    -> Target is NOT in the left sorted half.
    -> Search right half: left = mid + 1 = 4
  Active range: [4, 6] -> [0, 1, 2]

Iteration 2:
  left = 4, right = 6
  mid = 4 + (6 - 4) / 2 = 5
  nums = [4,  5,  6,  7,  0,  1,  2]
                          ↑   ↑   ↑
                        left mid right
  nums[mid] = 1 (1 != target 0)
  Check sorted half:
    nums[left] (0) <= nums[mid] (1) -> TRUE: Left half [0, 1] is sorted!
  Check target in left half:
    nums[left] (0) <= target (0) && target (0) < nums[mid] (1) -> TRUE (0 <= 0 < 1)
    -> Target IS in the left sorted half.
    -> Search left half: right = mid - 1 = 4
  Active range: [4, 4] -> [0]

Iteration 3:
  left = 4, right = 4
  mid = 4 + (4 - 4) / 2 = 4
  nums[mid] = nums[4] = 0
  Comparison: 0 == target 0 -> MATCH FOUND!
  -> Return mid = 4.
```

---

### The Architectural Pattern

```text
                   Search in Rotated Sorted Array
                                 ↓
                       while left <= right:
                                 ↓
                     mid = left + (right - left) / 2
                                 ↓
                       nums[mid] == target ?
                       /                 \
                  YES /                   \ NO
                     ↓                     ↓
                 return mid     Which half is sorted?
                                /                 \
           nums[left] <= nums[mid]                 nums[left] > nums[mid]
             (Left half sorted)                      (Right half sorted)
                     ↓                                       ↓
         target in [left, mid)?                  target in (mid, right]?
             /              \                        /              \
        YES /                \ NO               YES /                \ NO
           ↓                  ↓                    ↓                  ↓
     right = mid - 1    left = mid + 1       left = mid + 1     right = mid - 1
```

### Relationship with LeetCode 153
* **LeetCode 153 (Find Minimum):** Compares `nums[mid]` against `nums[right]` to locate the inflection/rotation boundary.
* **LeetCode 33 (Search Target):** Identifies which half is sorted first, then uses the bounds of that sorted half to route the search.

* **Next Review Date:** Low priority (benchmark rotated array target search pattern mastered).
* **Key Takeaway:** At every step in a rotated sorted array, at least one half is guaranteed to be sorted. Identify the sorted half, test if the target lies within its known numerical bounds, and branch accordingly in $O(\log N)$.
