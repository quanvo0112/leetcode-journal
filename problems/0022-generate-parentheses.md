# 0022. Generate Parentheses

- **Problem Link:** https://leetcode.com/problems/generate-parentheses/
- **Difficulty:** `Medium`
- **NeetCode Category:** `Backtracking`
- **LeetCode Topics:** `String` / `Dynamic Programming` / `Backtracking`
- **Core Pattern:** `Constrained Backtracking / DFS with Open & Close Counters`
- **Last Practiced:** 2026-10-02
- **Proficiency Level:**
  - [x] Level 1: Solved smoothly (< 20 mins, optimal)
  - [ ] Level 2: Struggled / Non-optimal / Edge-case bugs
  - [ ] Level 3: Needed editorial or hints

---

## 1. Pattern Recognition & Triggers

- **Clues in prompt:**
  - Given $n$ pairs of parentheses, write a function to generate all combinations of well-formed parentheses.
  - Return type is `vector<string>`.
  - Constraint: $1 \le n \le 8$.
- **Core intuition:**
  - This is an **enumeration** problem requiring every valid combination of $n$ matching bracket pairs (total length $2n$).
  - **Why not generate all and filter?** A brute-force algorithm generates all $2^{2n}$ possible strings of `'('` and `')'`, then validates each with a stack. This explores exponentially many invalid prefixes (such as `")("`, `"())"`), degrading performance to $O(2^{2n} \cdot n)$.
  - **Constrained Backtracking (Pruning at Generation Time):**
    - Track the number of open brackets used (`open`) and closed brackets used (`close`).
    - Constraint 1 (Quota): We cannot exceed $n$ pairs, so `open <= n` and `close <= n`.
    - Constraint 2 (Validity Invariant): At any intermediate prefix, we can never close more brackets than have been opened ($\text{close} \le \text{open}$). A `')'` is valid if and only if there is an unmatched `'('` preceding it ($\text{close} < \text{open}$).
    - Branching decisions:
      1. Add `'('` if `open < n`.
      2. Add `')'` if `close < open`.
    - Because invalid transitions are pruned upfront, **every leaf node that reaches length $2n$ is guaranteed to be well-formed**. Zero post-generation validation is required.
  - **Choose $\rightarrow$ Explore $\rightarrow$ Undo:**
    - Appending to a shared mutable `string current`, recursing, and immediately popping back (`current.pop_back()`) avoids costly string copying across recursion frames.

---

## 2. Approach & Trade-offs

1. **Approach 1 — Brute-Force Generation + Validation ($O(2^{2n} \cdot n)$ time, $O(2^{2n} \cdot n)$ space):**
   - Recursively generate all $2^{2n}$ binary sequences of `'('` and `')'`. Validate each string using a counter or stack.
   - *Drawback:* Exponentially wasteful. For $n = 8$, generates $2^{16} = 65,536$ strings while only $C_8 = 1,430$ are valid ($> 97\%$ discarded).

2. **Approach 2 — Dynamic Programming ($O(C_n \cdot n)$ time, $O(C_n \cdot n)$ space):**
   - Build valid strings using the recursive formulation:
     $$F(n) = \bigcup_{i=0}^{n-1} \left\{ \text{"("} + a + \text{")"} + b \mid a \in F(i), b \in F(n - 1 - i) \right\}$$
   - *Drawback:* Involves substantial intermediate vector allocations and string concatenations.

3. **Approach 3 — Constrained Backtracking with `open` / `close` Counters (Chosen Optimal Solution):**
   - Maintain a shared accumulator `string current`, recursive counters `open` and `close`.
   - If `current.size() == 2 * n`: save `current` to `result` and return.
   - If `open < n`: push `'('`, recurse with `open + 1`, pop back.
   - If `close < open`: push `')'`, recurse with `close + 1`, pop back.
   - *Verdict:* Optimal compute and memory footprint. Never constructs an invalid prefix, performs $O(1)$ push/pop mutations, and requires only $O(n)$ auxiliary recursion stack space.

---

## 3. Complexity Analysis

- **Time Complexity:** $O(C_n \cdot n) = O\left(\frac{4^n}{\sqrt{n}}\right)$
  - The number of valid well-formed parentheses strings of length $2n$ is given by the $n$-th **Catalan number**:
    $$C_n = \frac{1}{n + 1} \binom{2n}{n} \sim \frac{4^n}{n\sqrt{\pi n}} = O\left(\frac{4^n}{n^{3/2}}\right)$$
  - Each valid leaf node takes $O(n)$ time to copy the string of length $2n$ into `result`.
  - The total time is bounded by $O(C_n \cdot n)$, which is asymptotically optimal because every character in the output must be emitted.
- **Space Complexity:** $O(C_n \cdot n)$ total space / $O(n)$ auxiliary space
  - Output space: Stores $C_n$ strings of length $2n$.
  - Auxiliary memory: Recursion tree depth is strictly $2n$, and the shared `string current` occupies $2n$ characters $\implies O(n)$ auxiliary stack space.

---

## 4. Edge Cases & Gotchas

- [x] **Base Case ($n = 1$):** Generates exactly `["()"]`.
- [x] **Maximum Constraint ($n = 8$):** $C_8 = 1,430$ combinations, well within memory and runtime limits (< 5 ms).
- [x] **State Restoration (`pop_back()`):** Forgetting `current.pop_back()` pollutes the shared buffer, corrupting subsequent sibling branches.
- [x] **Strict Invariant (`close < open`):** Using `close <= open` would permit adding `')'` when `close == open`, instantly producing invalid prefixes like `")"`. The condition must strictly be `close < open`.

---

## 5. Clean Code (Optimal Solution: Constrained Backtracking)

```cpp
class Solution {
private:
    vector<string> result;
    string current;
    int n;

    void backtrack(int open, int close) {
        // A valid string has exactly n pairs (length 2 * n).
        if (current.size() == 2 * n) {
            result.push_back(current);
            return;
        }

        // We can add '(' if we still have opening brackets left.
        if (open < n) {
            current.push_back('(');
            backtrack(open + 1, close);
            current.pop_back();
        }

        // We can add ')' only if it will not make the string invalid.
        if (close < open) {
            current.push_back(')');
            backtrack(open, close + 1);
            current.pop_back();
        }
    }

public:
    vector<string> generateParenthesis(int n) {
        this->n = n;
        backtrack(0, 0);
        return result;
    }
};
```

---

## 6. Review & Takeaways

### Visual Recursion Tree ($n = 2$)

```text
                            "" (0, 0)
                                |
                             "(" (1, 0)
                           /           \
                 "((" (2, 0)            "()" (1, 1)
                     |                       |
                 "(()" (2, 1)           "()(" (2, 1)
                     |                       |
                "(())" (2, 2)           "()()" (2, 2)
                   [SAVE]                  [SAVE]

Final Result: ["(())", "()()"]
Total Generated: 2 (= C_2)
Total Invalid Explored: 0
```

---

### The Architectural Mental Model

```text
                       Generate Parentheses (n)
                                  ↓
                       Constrained Backtracking
                                  ↓
                        Track: open & close
                                  ↓
                    ┌───────────────────────────┐
                    │  current.size() == 2 * n  │──YES──> Save to result
                    └─────────────┬─────────────┘
                                  │ NO
                  ┌───────────────┴───────────────┐
                  ↓                               ↓
             open < n ?                      close < open ?
             /        \                      /            \
       YES  /          \  NO           YES  /              \  NO
           ↓            ↓                  ↓                ↓
      push '('        Skip            push ')'            Skip
      backtrack(open+1, close)        backtrack(open, close+1)
      pop_back()                      pop_back()
```

* **Next Review Date:** As needed / TBD
* **Key Takeaway:** Open bracket `'('` whenever quota remains (`open < n`); close bracket `')'` only when an open bracket is waiting to be matched (`close < open`). This ensures zero invalid prefixes are ever generated.
