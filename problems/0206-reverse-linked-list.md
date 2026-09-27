# 0206. Reverse Linked List

- **Problem Link:** https://leetcode.com/problems/reverse-linked-list/
- **Difficulty:** `Easy`
- **NeetCode Category:** `Linked List`
- **LeetCode Topics:** `Linked List` / `Recursion`
- **Core Pattern:** `Iterative In-Place Pointer Reversal (Three Pointers: prev, curr, next)`
- **Last Practiced:** 2026-09-27
- **Proficiency Level:**
  - [x] Level 1: Solved smoothly (< 20 mins, optimal)
  - [ ] Level 2: Struggled / Non-optimal / Edge-case bugs
  - [ ] Level 3: Needed editorial or hints

---

## 1. Pattern Recognition & Triggers

- **Clues in prompt:**
  - Given the `head` of a singly linked list, reverse the list, and return the reversed list.
  - Must transform $1 \to 2 \to 3 \to \text{nullptr}$ into $\text{nullptr} \leftarrow 1 \leftarrow 2 \leftarrow 3$.
- **Core intuition:**
  - Each node in a singly linked list only possesses a forward pointer (`curr->next`).
  - To reverse the list in-place, every pointer must be redirected backwards (`curr->next = prev`).
  - **The Pointer Severance Hazard:** If `curr->next` is overwritten immediately, the reference to the subsequent node is destroyed forever.
  - Hence, the fundamental invariant is to **temporarily cache `next = curr->next`** before redirecting the current pointer backwards, then shift both `prev` and `curr` forward.

---

## 2. Approach & Trade-offs

1. **Approach 1 — Recursive ($O(N)$ time, $O(N)$ space):**
   - Recurse to the tail of the list, then re-link nodes during stack unwinding:
     ```cpp
     ListNode* newHead = reverseList(head->next);
     head->next->next = head;
     head->next = nullptr;
     return newHead;
     ```
   - *Drawback:* Consumes $O(N)$ call stack frames. For deep lists ($N \ge 10^4$), recursion risks stack overflow (`SIGSEGV`).

2. **Approach 2 — Auxiliary Stack or Vector ($O(N)$ time, $O(N)$ space):**
   - Traverse the list and push all nodes or values into an auxiliary container, then pop or rebuild pointers.
   - *Drawback:* Wastes $O(N)$ auxiliary heap memory when pointers can easily be redirected in-place.

3. **Approach 3 — Iterative 3-Pointer In-Place Reversal (Chosen Optimal Solution):**
   - Maintain three pointers:
     - `prev`: tracks the head of the already reversed segment (starts as `nullptr`).
     - `curr`: tracks the current node being reversed (starts at `head`).
     - `next`: temporarily holds the reference to `curr->next` before breaking the link.
   - For each iteration:
     1. `ListNode* next = curr->next;` (Cache forward reference)
     2. `curr->next = prev;` (Redirect pointer backward)
     3. `prev = curr;` (Advance `prev` to include `curr`)
     4. `curr = next;` (Advance `curr` to the next unprocessed node)
   - When `curr == nullptr`, `prev` rests at the new head of the reversed list.
   - *Verdict:* Optimal $O(N)$ time, $O(1)$ space. Safe from stack overflow and trivial to recall during interviews.

---

## 3. Complexity Analysis

- **Time Complexity:** $O(N)$
  - Traverses the linked list of length $N$ exactly once. Each node undergoes constant $O(1)$ pointer manipulations.
- **Space Complexity:** $O(1)$
  - Operates strictly in-place using three auxiliary pointers (`prev`, `curr`, `next`) regardless of list size.

---

## 4. Edge Cases & Gotchas

- [x] **Empty List (`head == nullptr`):**
  - Loop condition `curr != nullptr` is immediately false. Returns `prev = nullptr` safely without dereferencing null pointers.
- [x] **Single-Node List (`head->next == nullptr`):**
  - Executes one iteration: `next = nullptr`, `curr->next = nullptr`, `prev = head`, `curr = nullptr`. Correctly returns the single node pointing to `nullptr`.
- [x] **Strict Assignment Order:**
  - The step sequence `next = curr->next` $\to$ `curr->next = prev` $\to$ `prev = curr` $\to$ `curr = next` must never be altered. Reassigning `curr->next` prior to caching `next` severs the list.
- [x] **Return Value Gotcha (`prev` vs. `curr`):**
  - The loop terminates when `curr == nullptr`. Returning `curr` returns `nullptr`. The new head is always `prev`.

---

## 5. Clean Code (Optimal Solution: Iterative 3 Pointers)

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
    ListNode* reverseList(ListNode* head) {
        ListNode* prev = nullptr;
        ListNode* curr = head;

        while (curr != nullptr) {
            // 1. Cache forward pointer before severing the link
            ListNode* next = curr->next;

            // 2. Reverse direction of current node
            curr->next = prev;

            // 3. Advance pointers forward
            prev = curr;
            curr = next;
        }

        // prev points to the new head of the reversed list
        return prev;
    }
};
```

---

## 6. Review & Takeaways

### Step-by-Step Dry Run

Given list: `1 -> 2 -> 3 -> nullptr`

```text
Initial State:
  prev = nullptr
  curr = 1 -> 2 -> 3 -> nullptr

Iteration 1:
  next = curr->next = 2
  curr->next = prev -> (1 -> nullptr)
  prev = curr = 1
  curr = next = 2
  State: nullptr <- 1    2 -> 3 -> nullptr
                   ^     ^
                  prev  curr

Iteration 2:
  next = curr->next = 3
  curr->next = prev -> (2 -> 1 -> nullptr)
  prev = curr = 2
  curr = next = 3
  State: nullptr <- 1 <- 2    3 -> nullptr
                         ^    ^
                        prev curr

Iteration 3:
  next = curr->next = nullptr
  curr->next = prev -> (3 -> 2 -> 1 -> nullptr)
  prev = curr = 3
  curr = next = nullptr
  State: nullptr <- 1 <- 2 <- 3
                              ^    ^
                             prev curr (nullptr)

Loop terminates (curr == nullptr).
Return prev (Node 3).
Final List: 3 -> 2 -> 1 -> nullptr.
```

---

### The Architectural Pattern

```text
                     Iterative Linked List Reversal
                                   ↓
                         Three Pointers Invariant
                                   ↓
                        prev  ←  curr  →  next
                                   ↓
                  ┌─────────────────────────────────┐
                  │ 1. next = curr->next;           │ (Save)
                  │ 2. curr->next = prev;           │ (Reverse)
                  │ 3. prev = curr;                 │ (Shift prev)
                  │ 4. curr = next;                 │ (Shift curr)
                  └─────────────────────────────────┘
                                   ↓
                         Repeat until curr == null
                                   ↓
                            Return prev (New Head)
```

* **Next Review Date:** Low priority (textbook foundational linked list pattern mastered).
* **Key Takeaway:** Always remember the four-line mantra: **Save `next` $\to$ reverse `curr->next` $\to$ shift `prev` $\to$ shift `curr`**. When `curr` reaches `nullptr`, `prev` is the new head.
