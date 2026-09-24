# 0020. Valid Parentheses

- **Problem Link:** https://leetcode.com/problems/valid-parentheses/
- **Difficulty:** `Easy`
- **NeetCode Category:** `Stack`
- **LeetCode Topics:** `String` / `Stack`
- **Core Pattern:** `LIFO Stack (Vector-backed, Push Opening / Match & Pop Closing)`
- **Last Practiced:** 2026-09-22
- **Proficiency Level:**
  - [x] Level 1: Solved smoothly (< 20 mins, optimal)
  - [ ] Level 2: Struggled / Non-optimal / Edge-case bugs
  - [ ] Level 3: Needed editorial or hints

---

## 1. Pattern Recognition & Triggers

- **Clues in prompt:** *"Given a string `s` containing just the characters '(', ')', '{', '}', '[' and ']'"*, *"open brackets must be closed by the same type of brackets"*, *"open brackets must be closed in the correct order"*, *"every close bracket has a corresponding open bracket of the same type"*.
- **Core intuition:**
  - Parentheses validation embodies the fundamental **LIFO (Last-In, First-Out)** principle:
    $$\text{The most recently opened bracket must be the first one to close.}$$
  - When encountering an opening bracket (`(`, `[`, `{`), we save it for future matching.
  - When encountering a closing bracket (`)`, `]`, `}`), it must match the opening bracket that was opened most recently.
  - This is the exact access pattern implemented by a **Stack**.

---

## 2. Approach & Trade-offs

1. **Approach 1 — String Replacement ($O(N^2)$ Time, $O(N)$ Space):**
   - Repeatedly find and replace `"()"`, `"{}"`, `"[]"` with `""` until the string no longer shrinks.
   - *Verdict:* Inefficient $O(N^2)$ due to string copying and repeated linear scans.

2. **Approach 2 — Stack using `std::stack<char>` ($O(N)$ Time, $O(N)$ Space):**
   - Push opening brackets, pop matching closing brackets.
   - *Verdict:* Completely correct, but `std::stack` is a container adaptor wrapping `std::deque` by default, adding minor abstraction overhead.

3. **Approach 3 — Stack using `std::vector<char>` (Optimal & Implemented):**
   - Use `vector<char> stack` as a lightweight stack using three primitives: `push_back()`, `back()`, and `pop_back()`.
   - Maintain direct `if` comparisons for bracket pairs instead of allocating an `unordered_map`.
   - *Verdict:* Optimal $O(N)$ time, $O(N)$ space. Minimal overhead, direct contiguous memory cache locality, zero dynamic hashing.

---

## 3. Complexity Analysis

- **Time Complexity:** $O(N)$
  - We iterate through the string of length $N$ exactly once.
  - For each character:
    - If opening: one `push_back()` operation ($O(1)$ amortized).
    - If closing: check emptiness ($O(1)$), read `back()` ($O(1)$), comparison ($O(1)$), and `pop_back()` ($O(1)$).
  - Overall time is strictly linear $O(N)$.
- **Space Complexity:** $O(N)$
  - In the worst case (e.g. all opening brackets `s = "(((((("`), the vector stores all $N$ characters.

---

## 4. Edge Cases & Gotchas

- [x] **Early Closing Bracket on Empty Stack (e.g. `s = ")"` or `s = "()]"`):**
  - If a closing bracket is encountered while `stack.empty()` is `true`, return `false` immediately. There is no opening bracket available to match.
- [x] **Type Mismatch (e.g. `s = "([)]"`):**
  - Top of stack is `[` but incoming bracket is `)`. `open != '('` triggers; correctly returns `false`.
- [x] **Unclosed Brackets at End (e.g. `s = "((("`):**
  - All characters were pushed, none were popped.
  - At loop termination, `return stack.empty();` correctly evaluates to `false` because remnants exist in the stack.
- [x] **Odd Length Strings:** An odd-length string cannot possibly be valid (optional early exit: `if (s.size() % 2 != 0) return false;`).
- [x] **Why `vector<char>` over `stack<char>`?**
  - `std::vector` allocates contiguous buffer space on the heap, guarantees cache locality, and exposes direct inspection without adaptor overhead.
- [x] **Why avoid `unordered_map` for 3 bracket types?**
  - Using a hash map `{ {')', '('}, ... }` introduces hash table lookups, memory allocations, and branching. Direct `if` statements run in near-zero CPU instructions.

---

## 5. Clean Code (Optimal Solution: Vector-based Stack)

```cpp
#include <string>
#include <vector>

using namespace std;

class Solution {
public:
    bool isValid(string s) {
        vector<char> stack;

        for (char c : s) {
            // Push opening brackets onto the stack
            if (c == '(' || c == '[' || c == '{') {
                stack.push_back(c);
            } else {
                // If closing bracket arrives but stack is empty -> invalid
                if (stack.empty()) {
                    return false;
                }

                char open = stack.back();
                stack.pop_back();

                // Verify that closing bracket matches the most recently opened bracket
                if ((c == ')' && open != '(') ||
                    (c == ']' && open != '[') ||
                    (c == '}' && open != '{')) {
                    return false;
                }
            }
        }

        // Valid only if all opened brackets have been successfully closed
        return stack.empty();
    }
};
```

---

## 6. Review & Takeaways

### Step-by-Step Dry Run

#### Case 1: `s = "([{}])"` (Valid)

```text
c = '(': opening -> push '('       -> stack: ['(']
c = '[': opening -> push '['       -> stack: ['(', '[']
c = '{': opening -> push '{'       -> stack: ['(', '[', '{']
c = '}': closing -> top='{', matches! pop '{' -> stack: ['(', '[']
c = ']': closing -> top='[', matches! pop '[' -> stack: ['(']
c = ')': closing -> top='(', matches! pop '(' -> stack: []

Loop finishes: stack is empty -> returns true.
```

#### Case 2: `s = "([)]"` (Mismatched Nesting)

```text
c = '(': opening -> push '('       -> stack: ['(']
c = '[': opening -> push '['       -> stack: ['(', '[']
c = ')': closing -> top='[' != '(' -> MISMATCH -> returns false.
```

---

### The Architectural Pattern

```text
Valid Parentheses
        ↓
   vector<char> stack
        ↓
  for c in s:
        ├─ is opening ('(', '[', '{')?
        │       └─ stack.push_back(c)
        └─ is closing (')', ']', '}')?
                ├─ stack.empty()? ── Yes ──> return false
                ├─ open = stack.back(); stack.pop_back()
                └─ open != match(c)? ── Yes ──> return false
        ↓
  return stack.empty()
```

* **Next Review Date:** Low priority (benchmark introductory stack pattern mastered).
* **Key Takeaway:** For any grammar, bracket, or nested syntax validation problem where "most recent open must close first", a **LIFO Stack** is the canonical optimal tool. Push opening tokens; pop and compare upon encountering closing tokens.
