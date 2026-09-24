# 0036. Valid Sudoku

- **Problem Link:** https://leetcode.com/problems/valid-sudoku/
- **Difficulty:** `Medium`
- **NeetCode Category:** `Arrays & Hashing`
- **LeetCode Topics:** `Array` / `Hash Table` / `Matrix`
- **Core Pattern:** `Bitmask / Hash Table (Row, Col, Box Encoding)`
- **Last Practiced:** 2026-09-19
- **Proficiency Level:**
  - [x] Level 1: Solved smoothly (< 20 mins, optimal)
  - [ ] Level 2: Struggled / Non-optimal / Edge-case bugs
  - [ ] Level 3: Needed editorial or hints

---

## 1. Pattern Recognition & Triggers
- Clues in prompt: *"Determine if a 9 x 9 Sudoku board is valid"*, *"Each row must contain digits 1-9 without repetition"*, *"Each column must contain digits 1-9 without repetition"*, *"Each of the nine 3 x 3 sub-boxes must contain digits 1-9 without repetition"*, *"Only the filled cells need to be validated"*.
- Core intuition: We must validate three orthogonal constraints across a fixed $9 \times 9$ grid: rows, columns, and $3 \times 3$ sub-boxes. Since each cell only contains digits `'1'` through `'9'` (a small, strictly bounded universe of 9 elements), the "seen" status of all 9 possible digits fits completely within a single 9-bit integer mask ($1 \ll \text{digit}$). We track 9 masks for rows, 9 for columns, and 9 for sub-boxes, validating and updating all 3 constraints in a single pass using ultra-fast bitwise operations.

---

## 2. Approach & Trade-offs

1. **Approach 1 — Hash Sets with String Keys (`unordered_set<string>`):**
   - Encode entries into strings like `"5 in row 0"`, `"5 in col 2"`, `"5 in box 0-0"`.
   - *Verdict:* Very concise to write in Python/JavaScript, but incurs heavy heap allocations, string concatenations, and dynamic hashing overhead in C++. Not recommended for C++ interviews.

2. **Approach 2 — 2D Boolean Arrays (`bool rows[9][9]`, `bool cols[9][9]`, `bool boxes[9][9]`):**
   - Allocate $3 \times 9 \times 9$ booleans (or integer counters) to track frequencies.
   - *Verdict:* $O(1)$ operations with zero dynamic allocation. Simple and robust, but consumes $243$ bytes of memory.

3. **Approach 3 — Bitmask + Single Pass (Optimal & Implemented):**
   - Maintain three arrays of 9 integers: `array<int, 9> rows`, `cols`, `boxes`.
   - Each integer acts as a 9-bit bitset where bit $k$ represents the presence of digit $k+1$.
   - For each non-empty cell:
     - Compute bit: `bit = 1 << (board[r][c] - '1')`.
     - Compute box ID: `box = (r / 3) * 3 + (c / 3)`.
     - Check: `(rows[r] & bit) || (cols[c] & bit) || (boxes[box] & bit)`.
     - Update: `rows[r] |= bit; cols[c] |= bit; boxes[box] |= bit;`.
   - *Verdict:* Minimizes memory to $27$ integers on the stack, avoids all hashing overhead, leverages CPU bitwise instructions, and processes the board in exactly 81 iterations.

---

## 3. Complexity Analysis

- **Time Complexity:** $O(1)$ — Strictly bounded by the fixed board size: $9 \times 9 = 81$ cells. Inside the loop, computing the box index, bit shifts, bitwise AND (`&`), and bitwise OR (`|=`) run in $O(1)$ machine instructions.
- **Space Complexity:** $O(1)$ — Uses three fixed arrays of 9 integers each (`array<int, 9>`):
  $$\text{Total auxiliary memory} = 3 \times 9 \times 4\text{ bytes} = 108\text{ bytes on the call stack}.$$
  Zero heap allocation.

---

## 4. Edge Cases & Gotchas
- [x] **Empty cells (`'.'`):** Must skip immediately with `continue` without updating any bitmask.
- [x] **Valid incomplete boards:** A board does not need to be completely filled or solvable; only existing filled digits are checked for mutual conflict.
- [x] **0-indexed vs 1-indexed digits:** Digits are characters `'1'` to `'9'`. Subtracting `'1'` (`board[r][c] - '1'`) maps digits cleanly into $[0, 8]$, fitting within bits $0$ to $8$.

---

## 5. Clean Code (Optimal Solution: Bitmask + Single Pass)

```cpp
class Solution {
public:
    bool isValidSudoku(vector<vector<char>>& board) {
        array<int, 9> rows{};
        array<int, 9> cols{};
        array<int, 9> boxes{};

        for (int r = 0; r < 9; ++r) {
            for (int c = 0; c < 9; ++c) {
                if (board[r][c] == '.') {
                    continue;
                }

                int digit = board[r][c] - '1'; // 0 to 8
                int bit = 1 << digit;          // 9-bit representation
                int box = (r / 3) * 3 + (c / 3);

                // If the digit is already set in current row, col, or 3x3 box
                if ((rows[r] & bit) || (cols[c] & bit) || (boxes[box] & bit)) {
                    return false;
                }

                // Mark digit as seen across all 3 constraints
                rows[r] |= bit;
                cols[c] |= bit;
                boxes[box] |= bit;
            }
        }

        return true;
    }
};
```

---

## 6. Review & Takeaways

### Visualizing the Bitmask Encoding

For any digit from $1$ to $9$, we map it to an offset $[0, 8]$ and shift:

```text
char c = '5';
int digit = '5' - '1'; // 4
int bit = 1 << 4;      // Binary: 000010000
```

If a row already contains digits $1$, $3$, and $5$:

```text
Digit:      9  8  7  6  5  4  3  2  1
Bit index:  8  7  6  5  4  3  2  1  0
Mask:       0  0  0  0  1  0  1  0  1  (Hex: 0x15)
```

- When encountering a new digit `X` with `bit = 1 << (X - '1')`:
  - `mask & bit != 0`: Digit already appeared $\rightarrow$ **conflict detected (`return false`)**.
  - `mask |= bit`: Bit flips from `0` to `1` $\rightarrow$ **digit recorded in $O(1)$**.

---

### The 3x3 Sub-Box Mapping Formula

The mapping formula:
```cpp
int box = (r / 3) * 3 + (c / 3);
```
projects any cell coordinate $(r, c) \in [0, 8] \times [0, 8]$ onto a unique box index $\in [0, 8]$:

```text
        c: 0 1 2   3 4 5   6 7 8
      +---------+---------+---------+
r: 0  |         |         |         |
   1  |  Box 0  |  Box 1  |  Box 2  |
   2  |         |         |         |
      +---------+---------+---------+
r: 3  |         |         |         |
   4  |  Box 3  |  Box 4  |  Box 5  |
   5  |         |         |         |
      +---------+---------+---------+
r: 6  |         |         |         |
   7  |  Box 6  |  Box 7  |  Box 8  |
   8  |         |         |         |
      +---------+---------+---------+
```

Examples:
- Cell $(0, 0) \rightarrow (0/3)*3 + (0/3) = 0*3 + 0 = \mathbf{0}$
- Cell $(0, 5) \rightarrow (0/3)*3 + (5/3) = 0*3 + 1 = \mathbf{1}$
- Cell $(4, 4) \rightarrow (4/3)*3 + (4/3) = 1*3 + 1 = \mathbf{4}$
- Cell $(8, 8) \rightarrow (8/3)*3 + (8/3) = 2*3 + 2 = \mathbf{8}$

---

### Interview Pitch: *"Why Bitmask over Hash Set?"*

> *"Because the Sudoku grid is fixed at $9 \times 9$ and the domain of values is strictly 9 digits, allocating dynamic collections like `unordered_set` creates unnecessary heap allocation, bucket pointer dereferencing, and hash calculations for each cell. By packing the presence of digits $1\text{–}9$ into a 9-bit integer mask, we achieve strictly zero heap allocation, cache-local operations in CPU registers, and validate all row, column, and sub-box constraints simultaneously in a single pass with pure bitwise AND and OR instructions."*

---

### The Core Architectural Pattern

```text
Fixed small domain (e.g., digits 1-9 or alphabet a-z)
     ↓
Represent "seen" state using bit positions (1 << val)
     ↓
Maintain one mask per constraint (rows, cols, boxes)
     ↓
Check with bitwise AND (&), update with bitwise OR (|=)
```

* **Next Review Date:** Low priority (benchmark bitmask constraint pattern mastered).
* **Key Takeaway:** Whenever an algorithm needs to track membership over a small, bounded universe ($\le 32$ or $\le 64$ distinct items), replace hash tables with primitive integer bitmasks.

