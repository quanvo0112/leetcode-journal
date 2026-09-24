# 0155. Min Stack

- **Problem Link:** https://leetcode.com/problems/min-stack/
- **Difficulty:** `Medium`
- **NeetCode Category:** `Stack`
- **LeetCode Topics:** `Stack` / `Design`
- **Core Pattern:** `Min Stack (Vector-backed Pair of {value, currentMin}, O(1) All Ops)`
- **Last Practiced:** 2026-09-23
- **Proficiency Level:**
  - [x] Level 1: Solved smoothly (< 20 mins, optimal)
  - [ ] Level 2: Struggled / Non-optimal / Edge-case bugs
  - [ ] Level 3: Needed editorial or hints

---

## 1. Pattern Recognition & Triggers

- **Clues in prompt:**
  - *"Design a stack that supports `push`, `pop`, `top`, and retrieving the minimum element in constant time."*
  - *"You must implement a solution with `O(1)` time complexity for each function."*
- **Core intuition:**
  - In a standard stack `[v1, v2, v3]`, finding the minimum element requires an $O(N)$ linear scan across all elements.
  - To achieve $O(1)$ retrieval without scanning, **each node must carry historical knowledge of the minimum value up to its level**.
  - Fundamental rule:
    $$\text{"Each node knows the minimum of the entire stack from the bottom up to itself."}$$
  - When a new element `val` is pushed:
    - If the stack is empty, the current minimum is simply `val`.
    - If the stack is non-empty, the new minimum is $\min(\text{val}, \text{currentMin of previous top})$.
  - When the top element is popped, the minimum naturally reverts to the previous element's stored minimum with **zero extra recalculation**.

---

## 2. Approach & Trade-offs

1. **Approach 1 — Naive Linear Scan ($O(1)$ Push/Pop/Top, $O(N)$ GetMin):**
   - Scan all elements on `getMin()`.
   - *Verdict:* Violates problem requirements ($O(1)$ strictly required for all operations).

2. **Approach 2 — Two Separate Stacks (`values` and `minValues`):**
   - Keep one stack for values and a parallel stack tracking minimums.
   - *Trade-off:* Requires manual synchronization across two containers during push and pop. Extra container bookkeeping overhead.

3. **Approach 3 — Single Vector of Pairs `std::vector<std::pair<int, int>>` (Optimal & Implemented):**
   - Each entry stores `{value, currentMin}`:
     - `stack.back().first` $\rightarrow$ `value`
     - `stack.back().second` $\rightarrow$ `currentMin`
   - *Verdict:* Optimal $O(1)$ for all operations, $O(N)$ space.
   - Co-locates `(value, currentMin)` in contiguous cache-friendly memory. Zero synchronization risk between two containers. No pointer overhead.

---

## 3. Complexity Analysis

- **Time Complexity:** $O(1)$ for all 4 operations:
  - `push(val)`: $O(1)$ amortized (`vector::push_back` of a `pair<int, int>`).
  - `pop()`: $O(1)$ (`vector::pop_back`).
  - `top()`: $O(1)$ (direct vector index read `back().first`).
  - `getMin()`: $O(1)$ (direct vector index read `back().second`).
- **Space Complexity:** $O(N)$
  - Stores each value alongside one extra 4-byte `int` for the prefix minimum up to that point. Strictly satisfies the constraint.

---

## 4. Edge Cases & Gotchas

- [x] **First element pushed into an empty stack:**
  - Cannot access `stack.back().second` on an empty container. Use ternary check: `stack.empty() ? val : min(val, stack.back().second)`.
- [x] **Negative numbers & integer bounds:**
  - Values fit within standard signed 32-bit integer ranges `[-2^31, 2^31 - 1]`. `min()` correctly compares signed negatives without underflow/overflow.
- [x] **Repeated identical values:**
  - If identical minimum elements are pushed (e.g. `push(2), push(2)`), both nodes record `currentMin = 2`. When one is popped, the remaining one still safely holds `currentMin = 2`.
- [x] **Calling `pop()`, `top()`, `getMin()` on empty stack:**
  - LeetCode problem constraints guarantee that `pop()`, `top()`, and `getMin()` are always called on non-empty stacks.

---

## 5. Clean Code (Optimal Solution: Single Vector of Pairs)

```cpp
#include <vector>
#include <utility>
#include <algorithm>

using namespace std;

class MinStack {
private:
    // Each element stores: {value, currentMin from bottom up to this element}
    vector<pair<int, int>> stack;

public:
    MinStack() {
    }

    void push(int val) {
        int currentMin = stack.empty() ? val : min(val, stack.back().second);
        stack.push_back({val, currentMin});
    }

    void pop() {
        stack.pop_back();
    }

    int top() {
        return stack.back().first;
    }

    int getMin() {
        return stack.back().second;
    }
};
```

---

## 6. Review & Takeaways

### Step-by-Step Dry Run

Example sequence: `push(-2) -> push(0) -> push(-3) -> getMin() -> pop() -> top() -> getMin()`

```text
1. push(-2):
   - stack empty -> currentMin = -2
   - stack: [ (-2, -2) ]

2. push(0):
   - currentMin = min(0, -2) = -2
   - stack: [ (-2, -2), (0, -2) ]

3. push(-3):
   - currentMin = min(-3, -2) = -3
   - stack: [ (-2, -2), (0, -2), (-3, -3) ]

4. getMin():
   - return stack.back().second = -3  (O(1))

5. pop():
   - remove (-3, -3)
   - stack: [ (-2, -2), (0, -2) ]
   - Notice: minimum automatically reverts to -2 without recalculation!

6. top():
   - return stack.back().first = 0    (O(1))

7. getMin():
   - return stack.back().second = -2  (O(1))
```

---

### The Architectural Pattern

```text
                  MinStack Design
                         ↓
             vector<pair<int, int>>
            ┌────────────┬────────────┐
            │   value    │ currentMin │
            └────────────┴────────────┘
                         ↓
  push(val):
    currentMin = stack.empty() ? val : min(val, stack.back().second)
    stack.push_back({val, currentMin})
                         ↓
  pop():
    stack.pop_back()  ──> automatically restores previous state
                         ↓
  top():
    return stack.back().first
                         ↓
  getMin():
    return stack.back().second
```

* **Next Review Date:** Low priority (canonical stack state-tracking design pattern mastered).
* **Key Takeaway:** Whenever an algorithm needs instantaneous aggregate queries (like minimum, maximum, or prefix sum) over a stack, **piggyback the prefix aggregate onto each element**. The LIFO property guarantees that popping an element restores the exact prior aggregate state in $O(1)$.
