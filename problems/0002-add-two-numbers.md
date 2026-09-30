# 0002. Add Two Numbers

- **Problem Link:** https://leetcode.com/problems/add-two-numbers/
- **Difficulty:** `Medium`
- **NeetCode Category:** `Linked List`
- **LeetCode Topics:** `Linked List` / `Math` / `Recursion`
- **Core Pattern:** `Simulated Elementary Math (Digit-by-Digit Addition with Carry) + Dummy Head Node`
- **Last Practiced:** 2026-09-30
- **Proficiency Level:**
  - [x] Level 1: Solved smoothly (< 20 mins, optimal)
  - [ ] Level 2: Struggled / Non-optimal / Edge-case bugs
  - [ ] Level 3: Needed editorial or hints

---

## 1. Pattern Recognition & Triggers

- **Clues in prompt:**
  - You are given two non-empty linked lists representing two non-negative integers.
  - The digits are stored in **reverse order**, and each node contains a single digit.
  - Add the two numbers and return the sum as a linked list.
- **Core intuition:**
  - In positional base-10 arithmetic, manual column addition starts from the least significant digit (ones place) and proceeds toward the most significant digit, carrying over any excess $\ge 10$.
  - Because the linked lists store digits in reverse order, the list heads represent the ones digit, perfectly aligning with column-by-column addition:
    $$\text{sum} = \text{carry} + (\text{l1 ? l1->val : 0}) + (\text{l2 ? l2->val : 0})$$
    $$\text{digit} = \text{sum} \pmod{10}$$
    $$\text{carry} = \lfloor \text{sum} / 10 \rfloor$$
  - **The Lingering Carry Invariant:** The iteration cannot terminate merely because `l1` and `l2` have reached `nullptr`. If a carry remains ($\text{carry} > 0$), a final node must be allocated (e.g., $999 + 1 = 1000$).
  - Hence, the loop guard must encompass all three sources: `while (l1 || l2 || carry)`.
  - A stack-allocated **dummy node** (`ListNode dummy; ListNode* curr = &dummy;`) avoids edge cases when building the result head.

---

## 2. Approach & Trade-offs

1. **Approach 1 — Conversion to Integer ($O(M + N)$ time, Overflow Hazard):**
   - Traverse lists to reconstruct standard integers, add them, and convert the sum back into a linked list.
   - *Drawback:* The number of nodes can reach $100$. Standard 64-bit integer types (`long long`, `unsigned long long`, `__int128`) will overflow catastrophically.

2. **Approach 2 — Recursive Column Addition ($O(\max(M, N))$ time, $O(\max(M, N))$ space):**
   - Recurse through `l1->next` and `l2->next` while passing `carry` down the call stack.
   - *Drawback:* Consumes $O(\max(M, N))$ call stack frames. Unnecessary recursion overhead when an iterative loop is straightforward.

3. **Approach 3 — Iterative + Dummy Node + Carry (Chosen Optimal Solution):**
   - Maintain a local stack dummy node `ListNode dummy;` with `curr = &dummy;` and `carry = 0;`.
   - Loop while `l1 || l2 || carry`:
     - Initialize `sum = carry`.
     - If `l1` is non-null, add `l1->val` and advance `l1 = l1->next`.
     - If `l2` is non-null, add `l2->val` and advance `l2 = l2->next`.
     - Append the new digit: `curr->next = new ListNode(sum % 10); curr = curr->next;`.
     - Compute the forward carry: `carry = sum / 10;`.
   - Return `dummy.next`.
   - *Verdict:* Optimal $O(\max(M, N))$ time, $O(1)$ auxiliary working space, clean C++ memory allocation for the output list, and uniform handling of unequal list lengths and trailing carries.

---

## 3. Complexity Analysis

- **Time Complexity:** $O(\max(M, N))$
  - Where $M$ and $N$ are the lengths of `l1` and `l2` respectively. The loop executes $\max(M, N)$ times (or $\max(M, N) + 1$ if an additional carry digit is produced at the end).
- **Space Complexity:** $O(\max(M, N))$ Output Space / $O(1)$ Auxiliary Space
  - The output linked list requires at most $\max(M, N) + 1$ new nodes. The auxiliary working memory aside from the returned list is strictly $O(1)$ (`dummy`, `curr`, `carry`, `sum`).

---

## 4. Edge Cases & Gotchas

- [x] **Unequal List Lengths (e.g. `99 + 1 = 100`):**
  - Handled naturally by the independent `if (l1)` and `if (l2)` branches. The shorter list stops contributing digits once exhausted, while the longer list continues absorbing the carry.
- [x] **Trailing Carry at Most Significant Digit (e.g. `999 + 1 = 1000`):**
  - The condition `while (l1 || l2 || carry)` guarantees that when both lists are `nullptr` but `carry == 1`, an extra iteration runs and appends the final `1` node.
- [x] **Single-Digit Zeros (`0 + 0 = 0`):**
  - Runs exactly one iteration: `sum = 0`, creates node `0`, `carry = 0`, loop terminates.
- [x] **Input Immutability:**
  - Fresh nodes are allocated (`new ListNode(...)`) rather than mutating `l1` or `l2`, preserving caller data integrity.
- [x] **Stack Dummy Safety:**
  - Using a local stack-allocated `ListNode dummy;` avoids memory leaks for the dummy sentinel itself while returning `dummy.next` safely.

---

## 5. Clean Code (Optimal Solution: Iterative + Dummy Node + Carry)

```cpp
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */
class Solution {
public:
    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
        ListNode dummy;
        ListNode* curr = &dummy;

        int carry = 0;

        // Continue as long as there is an input digit or a lingering carry
        while (l1 || l2 || carry) {
            int sum = carry;

            if (l1) {
                sum += l1->val;
                l1 = l1->next;
            }

            if (l2) {
                sum += l2->val;
                l2 = l2->next;
            }

            // Create new node with the current digit
            curr->next = new ListNode(sum % 10);
            curr = curr->next;

            // Carry over to the next column
            carry = sum / 10;
        }

        return dummy.next;
    }
};
```

---

## 6. Review & Takeaways

### Step-by-Step Dry Run

#### Example 1: `l1 = [2, 4, 3]`, `l2 = [5, 6, 4]` (Represents $342 + 465 = 807$)

```text
Initial State:
  dummy -> nullptr, curr = &dummy, carry = 0

Iteration 1:
  sum = carry (0) + l1->val (2) + l2->val (5) = 7
  digit = 7 % 10 = 7
  carry = 7 / 10 = 0
  curr->next = Node(7)
  Merged: dummy -> 7

Iteration 2:
  sum = carry (0) + l1->val (4) + l2->val (6) = 10
  digit = 10 % 10 = 0
  carry = 10 / 10 = 1
  curr->next = Node(0)
  Merged: dummy -> 7 -> 0

Iteration 3:
  sum = carry (1) + l1->val (3) + l2->val (4) = 8
  digit = 8 % 10 = 8
  carry = 8 / 10 = 0
  curr->next = Node(8)
  Merged: dummy -> 7 -> 0 -> 8

Loop terminates (l1 == null, l2 == null, carry == 0).
Return dummy.next: 7 -> 0 -> 8 (Represents 807).
```

#### Example 2: Trailing Carry Propagation (`l1 = [9, 9, 9]`, `l2 = [1]`)

```text
Iter 1: 9 + 1 + 0 = 10 -> Node(0), carry = 1
Iter 2: 9 + 0 + 1 = 10 -> Node(0), carry = 1
Iter 3: 9 + 0 + 1 = 10 -> Node(0), carry = 1
Iter 4: l1=null, l2=null, carry=1 -> 0 + 0 + 1 = 1 -> Node(1), carry = 0
Result: 0 -> 0 -> 0 -> 1 (Represents 1000).
```

---

### The Architectural Pattern

```text
                         Add Two Numbers
                                ↓
                        ListNode dummy;
                       curr = &dummy;
                         carry = 0;
                                ↓
                   while (l1 || l2 || carry):
                                ↓
                   sum = carry + l1.val + l2.val
                                ↓
                       ┌─────────────────┐
                       │ digit = sum % 10│ ──> curr->next = new Node(digit)
                       │ carry = sum / 10│ ──> pass to next column
                       └─────────────────┘
                                ↓
                         curr = curr->next
                                ↓
                        return dummy.next
```

* **Next Review Date:** Low priority (standard simulated math addition pattern mastered).
* **Key Takeaway:** Traverse digit-by-digit from least to most significant, create nodes with `sum % 10`, propagate `sum / 10`, and always maintain `|| carry` in the loop condition to naturally handle trailing most significant carries ($999 + 1 = 1000$) without special branching.
