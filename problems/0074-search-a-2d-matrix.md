# 0074. Search a 2D Matrix

- **Problem Link:** https://leetcode.com/problems/search-a-2d-matrix/
- **Difficulty:** `Medium`
- **NeetCode Category:** `Binary Search`
- **LeetCode Topics:** `Array` / `Binary Search` / `Matrix`
- **Core Pattern:** `Virtual 1D Binary Search via 2D Index Mapping (row = mid / cols, col = mid % cols)`
- **Last Practiced:** 2026-09-25
- **Proficiency Level:**
  - [x] Level 1: Solved smoothly (< 20 mins, optimal)
  - [ ] Level 2: Struggled / Non-optimal / Edge-case bugs
  - [ ] Level 3: Needed editorial or hints

---

## 1. Pattern Recognition & Triggers

- **Clues in prompt:**
  - *"Each row is sorted in non-decreasing order."*
  - *"The first integer of each row is greater than the last integer of the previous row."*
  - *"You must write a solution in $O(\log(m \times n))$ time complexity."*
- **Core intuition:**
  - The two problem guarantees mean that if you read the matrix row by row from top-left to bottom-right, all $m \times n$ values form a **single contiguous, strictly non-decreasing 1D sequence**.
  - We do not need to create or copy the elements into a real 1D array.
  - Instead, we can run a standard binary search on the virtual index range $[0, m \times n - 1]$.
  - Any 1D index `mid` maps directly to its 2D matrix coordinates in $O(1)$ arithmetic:
    $$\text{row} = \lfloor \text{mid} / \text{cols} \rfloor$$
    $$\text{col} = \text{mid} \pmod{\text{cols}}$$

---

## 2. Approach & Trade-offs

1. **Approach 1 — Brute-Force 2D Scan ($O(m \times n)$ Time, $O(1)$ Space):**
   - Iterate through every row and column until target is found or matrix ends.
   - *Verdict:* Violates the strict $O(\log(m \times n))$ requirement; ignores both sorted invariants.

2. **Approach 2 — Two-Pass Binary Search ($O(\log m + \log n)$ Time, $O(1)$ Space):**
   - First binary search across the first column of all rows to locate the specific row that could contain `target`.
   - Then binary search within that identified row.
   - *Verdict:* Achieves $O(\log m + \log n) = O(\log(m \times n))$, but requires two separate search procedures, extra boundary logic, and is more error-prone than a single pass.

3. **Approach 3 — Virtual 1D Binary Search (Chosen Optimal Solution):**
   - Define virtual search boundaries: `left = 0`, `right = rows * cols - 1`.
   - While `left <= right`:
     - Calculate safe midpoint: `mid = left + (right - left) / 2`.
     - Map `mid` to 2D indices: `row = mid / cols`, `col = mid % cols`.
     - Compare `matrix[row][col]` with `target`:
       - If equal: return `true`.
       - If `< target`: `left = mid + 1`.
       - If `> target`: `right = mid - 1`.
   - *Verdict:* Optimal $O(\log(m \times n))$ Time, $O(1)$ Auxiliary Space. One single standard binary search loop with zero extra memory allocations.

---

## 3. Complexity Analysis

- **Time Complexity:** $O(\log(m \times n))$
  - The virtual search space has size $N = m \times n$.
  - Each step of binary search halves this search space, executing at most $\lfloor \log_2(m \times n) \rfloor + 1$ iterations.
  - Coordinate conversions (`/` and `%`) execute in $O(1)$ time.
- **Space Complexity:** $O(1)$
  - No physical array is flattened or allocated; only scalar integer variables (`rows`, `cols`, `left`, `right`, `mid`, `row`, `col`) are kept on the stack.

---

## 4. Edge Cases & Gotchas

- [x] **$1 \times 1$ Matrix (e.g. `matrix = [[1]], target = 1`):**
  - `rows = 1, cols = 1, left = 0, right = 0`.
  - Midpoint evaluates at index 0 (`row = 0, col = 0`), matching immediately and returning `true`.
- [x] **Target Smaller than Minimum Element (`target < matrix[0][0]`):**
  - Midpoint values will always be `> target`, causing `right` to decrement down to `-1`, terminating the loop and returning `false`.
- [x] **Target Larger than Maximum Element (`target > matrix[m-1][n-1]`):**
  - Midpoint values will always be `< target`, causing `left` to increment past $m \times n - 1$, terminating the loop and returning `false`.
- [x] **Integer Overflow in `rows * cols`:**
  - Matrix dimensions are constrained to $m, n \le 100 \implies m \times n \le 10^4$, fitting well within standard 32-bit signed integer limits ($2 \times 10^9$).

---

## 5. Clean Code (Optimal Solution: Virtual 1D Binary Search)

```cpp
#include <vector>

using namespace std;

class Solution {
public:
    bool searchMatrix(vector<vector<int>>& matrix, int target) {
        int rows = matrix.size();
        int cols = matrix[0].size();

        // Search space is the virtual 1D closed interval [0, rows * cols - 1]
        int left = 0;
        int right = rows * cols - 1;

        while (left <= right) {
            int mid = left + (right - left) / 2;

            // Map 1D virtual index to 2D matrix coordinates
            int row = mid / cols;
            int col = mid % cols;

            if (matrix[row][col] == target) {
                return true;
            }

            if (matrix[row][col] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }

        return false; // Target not found
    }
};
```

---

## 6. Review & Takeaways

### Step-by-Step Dry Run

Given `matrix = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]`, `target = 16`:

```text
Dimensions: rows = 3, cols = 4 -> total elements = 12
Initial interval: left = 0, right = 11

Iteration 1:
  mid = 0 + (11 - 0) / 2 = 5
  Coordinate mapping:
    row = 5 / 4 = 1
    col = 5 % 4 = 1
  matrix[1][1] = 11
  Comparison: 11 < 16 (matrix[row][col] < target)
  -> Target lies strictly in the right half.
  -> left = mid + 1 = 6

Iteration 2:
  left = 6, right = 11
  mid = 6 + (11 - 6) / 2 = 8
  Coordinate mapping:
    row = 8 / 4 = 2
    col = 8 % 4 = 0
  matrix[2][0] = 23
  Comparison: 23 > 16 (matrix[row][col] > target)
  -> Target lies strictly in the left half.
  -> right = mid - 1 = 7

Iteration 3:
  left = 6, right = 7
  mid = 6 + (7 - 6) / 2 = 6
  Coordinate mapping:
    row = 6 / 4 = 1
    col = 6 % 4 = 2
  matrix[1][2] = 16
  Comparison: 16 == 16 (matrix[row][col] == target)
  -> Match found!
  -> Return true.
```

---

### The Architectural Pattern

```text
                     2D Matrix (m rows x n cols)
                     (Strict row-to-row ordering)
                                 ↓
                  Virtual 1D Range: [0 ... m*n - 1]
                                 ↓
                        while left <= right:
                                 ↓
                     mid = left + (right - left) / 2
                                 ↓
                      Index Transformation:
                        row = mid / cols
                        col = mid % cols
                                 ↓
                  matrix[row][col] vs target
                 /             |             \
                /              |              \
               <               ==              >
              ↓                ↓                ↓
        left = mid + 1    return true     right = mid - 1
```

* **Next Review Date:** Low priority (benchmark virtual index projection binary search pattern mastered).
* **Key Takeaway:** When a 2D matrix satisfies both row-wise sorting and strict row-to-row chain ordering, treat it as a flattened 1D array using `row = mid / cols` and `col = mid % cols` to perform a single clean binary search in $O(\log(m \times n))$.
