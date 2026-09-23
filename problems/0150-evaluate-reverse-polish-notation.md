# 0150. Evaluate Reverse Polish Notation

- **Problem Link:** https://leetcode.com/problems/evaluate-reverse-polish-notation/
- **Difficulty:** `Medium`
- **NeetCode Category:** `Stack`
- **LeetCode Topics:** `Array` / `Math` / `Stack`
- **Core Pattern:** `Stack-Based Arithmetic Expression Evaluation (Pop Right, Pop Left, Push Result)`
- **Last Practiced:** 2026-09-23
- **Proficiency Level:** 
  - [x] Level 1: Solved smoothly (< 20 mins, optimal)
  - [ ] Level 2: Struggled / Non-optimal / Edge-case bugs
  - [ ] Level 3: Needed editorial or hints

---

## 1. Pattern Recognition & Triggers

- **Clues in prompt:**
  - *"You are given an array of strings `tokens` that represents an arithmetic expression in a Reverse Polish Notation."*
  - *"Evaluate the expression. Return an integer that represents the value of the expression."*
  - *"Valid operators are '+', '-', '*', and '/'. Each operand may be an integer or another expression."*
  - *"Division between two integers always truncates toward zero."*
- **Core intuition:**
  - In **Reverse Polish Notation (RPN)** (postfix notation), operators follow their operands (e.g. `2 1 +` means `2 + 1`).
  - This eliminates the need for parentheses and operator precedence rules.
  - The evaluation order is naturally modeled by a **Stack**:
    - **Operands (numbers)** are pushed onto the stack as they arrive.
    - **Operators** immediately consume the two most recent operands from the top of the stack, compute the operation, and push the intermediate result back onto the stack.
  - At the end of evaluation, exactly one value remains in the stack, which is the final expression result.

---

## 2. Approach & Trade-offs

1. **Approach 1 — Recursive String Replacement / Parsing:**
   - Scan for the first operator, evaluate with the two preceding numbers, replace the 3 tokens with the result, and repeat.
   - *Verdict:* Inefficient $O(N^2)$ due to array/string shifting and repeated traversals.

2. **Approach 2 — Vector-backed Stack (`std::vector<int>`) (Optimal & Implemented):**
   - Traverse the `tokens` array linearly from left to right.
   - If token is an operator:
     - Pop `right = stack.back(); stack.pop_back();`
     - Pop `left = stack.back(); stack.pop_back();`
     - Compute `left <op> right` and push result back onto stack.
   - If token is an integer string:
     - Convert using `stoi(token)` and push onto stack.
   - *Verdict:* Optimal $O(N)$ Time, $O(N)$ Space. Each token is visited and processed once.

---

## 3. Complexity Analysis

- **Time Complexity:** $O(N)$
  - We iterate through $N$ tokens exactly once.
  - For each token:
    - String equality check: $O(1)$.
    - Number conversion (`stoi`): $O(L)$ where $L \le 5$ (length of string), effectively $O(1)$.
    - Stack `push_back()`, `back()`, `pop_back()`: $O(1)$ amortized.
    - Arithmetic operations: $O(1)$.
  - Total time complexity is strictly linear $O(N)$.
- **Space Complexity:** $O(N)$
  - In the worst-case scenario (e.g. all numbers followed by all operators), the stack stores up to $(N + 1) / 2$ elements ($O(N)$ auxiliary space).

---

## 4. Edge Cases & Gotchas

- [x] **Operand Order (The #1 Most Common Bug):**
  - Stacks are LIFO. The **first** element popped is the **right** operand; the **second** element popped is the **left** operand.
  - For subtraction and division, operand order is non-commutative:
    - `left - right` (NOT `right - left`).
    - `left / right` (NOT `right / left`).
  - Example: `["6", "4", "-"]` $\rightarrow$ pop `right = 4`, pop `left = 6` $\rightarrow$ `6 - 4 = 2`.
- [x] **Division Truncation Toward Zero:**
  - The problem requires truncation toward zero (e.g. `13 / 5 = 2`, `-13 / 5 = -2`).
  - In C++11 and later (including C++17), integer division between signed `int` types is guaranteed to **truncate toward zero**. No special handling like `floor()` or `trunc()` is required.
- [x] **Negative Numbers as Operands:**
  - Negative integers like `"-11"` start with `'-'`, but are tokens of length $> 1$ or distinct from operator string `"-"`. Using direct token equality `token == "-"` cleanly distinguishes the subtraction operator from negative numeric values.
- [x] **Single-Element Expressions:**
  - If `tokens = ["42"]`, no operators are executed. The number is pushed and immediately returned from `stack.back()`.

---

## 5. Clean Code (Optimal Solution: Vector-backed Stack)

```cpp
#include <vector>
#include <string>

using namespace std;

class Solution {
public:
    int evalRPN(vector<string>& tokens) {
        vector<int> stack;

        for (const string& token : tokens) {
            if (token == "+" || token == "-" || token == "*" || token == "/") {
                // Top of stack is the RIGHT operand; next is the LEFT operand
                int right = stack.back();
                stack.pop_back();
                int left = stack.back();
                stack.pop_back();

                if (token == "+") {
                    stack.push_back(left + right);
                } else if (token == "-") {
                    stack.push_back(left - right);
                } else if (token == "*") {
                    stack.push_back(left * right);
                } else {
                    stack.push_back(left / right);
                }
            } else {
                stack.push_back(stoi(token));
            }
        }

        return stack.back();
    }
};
```

---

## 6. Review & Takeaways

### Step-by-Step Dry Run

#### Case 1: `tokens = ["2", "1", "+", "3", "*"]`

```text
token = "2": number   -> push 2                  -> stack: [2]
token = "1": number   -> push 1                  -> stack: [2, 1]
token = "+": operator -> right = 1, left = 2
                         2 + 1 = 3 -> push 3      -> stack: [3]
token = "3": number   -> push 3                  -> stack: [3, 3]
token = "*": operator -> right = 3, left = 3
                         3 * 3 = 9 -> push 9      -> stack: [9]

Result: stack.back() = 9.
```

#### Case 2: `tokens = ["4", "13", "5", "/", "+"]`

```text
token = "4":  push 4                             -> stack: [4]
token = "13": push 13                            -> stack: [4, 13]
token = "5":  push 5                             -> stack: [4, 13, 5]
token = "/":  right = 5, left = 13
              13 / 5 = 2 -> push 2               -> stack: [4, 2]
token = "+":  right = 2, left = 4
              4 + 2 = 6 -> push 6                -> stack: [6]

Result: stack.back() = 6.
```

---

### The Architectural Pattern

```text
              Evaluate Reverse Polish Notation
                             ↓
                     vector<int> stack
                             ↓
                  for each token in tokens:
                   /                       \
          is operator?                   is number?
         /            \                      ↓
       Yes             No             stack.push_back(stoi)
        ↓
   right = pop()
   left  = pop()
   result = left <op> right
   stack.push_back(result)
        ↓
   return stack.back()
```

* **Next Review Date:** Low priority (benchmark postfix expression evaluation pattern mastered).
* **Key Takeaway:** For any postfix/RPN expression evaluation, a stack is the canonical data structure. Always remember: **the first popped element is the right-hand side operand (`right`), and the second popped element is the left-hand side operand (`left`)**.
