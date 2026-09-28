# 0021. Merge Two Sorted Lists

- **Problem Link:** https://leetcode.com/problems/merge-two-sorted-lists/
- **Difficulty:** `Easy`
- **NeetCode Category:** `Linked List`
- **LeetCode Topics:** `Linked List` / `Recursion`
- **Core Pattern:** `Iterative In-Place Merge with Dummy Head Pointer (Two Pointers)`
- **Last Practiced:** 2026-09-28
- **Proficiency Level:**
  - [x] Level 1: Solved smoothly (< 20 mins, optimal)
  - [ ] Level 2: Struggled / Non-optimal / Edge-case bugs
  - [ ] Level 3: Needed editorial or hints

---

## 1. Pattern Recognition & Triggers

- **Clues in prompt:**
  - Given the heads of two sorted linked lists `list1` and `list2`.
  - Merge the two lists into one sorted list by splicing together the nodes of the first two lists.
  - Return the head of the merged linked list.
- **Core intuition:**
  - Both input lists are already sorted in ascending order.
  - At each step, the next smallest element in the merged sequence must be either the current head of `list1` or `list2`.
  - We do not need to construct new nodes via heap allocation; we simply splice existing nodes by adjusting their `next` pointers.
  - A local stack-allocated **dummy node** (`ListNode dummy; ListNode* curr = &dummy;`) eliminates boilerplate edge-case checks for initializing the head of the merged list.
  - Once either list runs out of nodes, the non-empty list is already completely sorted and can be spliced in $O(1)$ time with `curr->next = list1 ? list1 : list2;`.

---

## 2. Approach & Trade-offs

1. **Approach 1 — Allocate New Nodes ($O(N + M)$ time, $O(N + M)$ space):**
   - Create a `new ListNode(...)` for every value extracted from both lists.
   - *Drawback:* Pointlessly allocates heap memory, creates garbage collection / memory management overhead, and violates the in-place splicing requirement.

2. **Approach 2 — Recursive Merge ($O(N + M)$ time, $O(N + M)$ space):**
   - Compare heads and recurse:
     ```cpp
     if (!list1) return list2;
     if (!list2) return list1;
     if (list1->val <= list2->val) {
         list1->next = mergeTwoLists(list1->next, list2);
         return list1;
     } else {
         list2->next = mergeTwoLists(list1, list2->next);
         return list2;
     }
     ```
   - *Drawback:* Consumes $O(N + M)$ call stack frames, exposing the solution to potential stack overflow on deep inputs.

3. **Approach 3 — Iterative In-Place Merge with Dummy Node (Chosen Optimal Solution):**
   - Instantiate a lightweight `dummy` node on the stack and maintain pointer `curr = &dummy`.
   - While both `list1` and `list2` are non-null:
     - If `list1->val <= list2->val`: attach `list1` (`curr->next = list1`), advance `list1 = list1->next`.
     - Else: attach `list2` (`curr->next = list2`), advance `list2 = list2->next`.
     - Advance `curr = curr->next`.
   - Once the loop terminates, at most one list has remaining nodes. Splice it directly: `curr->next = list1 ? list1 : list2;`.
   - Return `dummy.next`.
   - *Verdict:* Optimal $O(N + M)$ time and $O(1)$ auxiliary space. Zero heap allocation, completely safe from stack overflow, and simple to implement cleanly.

---

## 3. Complexity Analysis

- **Time Complexity:** $O(N + M)$
  - Where $N$ and $M$ represent the lengths of `list1` and `list2` respectively. Each node comparison advances one pointer forward. At most $N + M$ comparisons occur, followed by an $O(1)$ tail link.
- **Space Complexity:** $O(1)$
  - Operates strictly in-place by rewiring existing node pointers. Only a stack-allocated dummy node and auxiliary pointer `curr` are used.

---

## 4. Edge Cases & Gotchas

- [x] **Both Lists Empty (`list1 == nullptr && list2 == nullptr`):**
  - Loop does not execute. `curr->next = nullptr ? nullptr : nullptr;` sets `curr->next = nullptr`. Returns `dummy.next` which is `nullptr`.
- [x] **One List Empty (`list1 == nullptr` or `list2 == nullptr`):**
  - Loop is bypassed. The non-empty list is attached immediately to `curr->next`. Returns the non-empty list's head in $O(1)$ time.
- [x] **Lists of Unequal Lengths:**
  - Handled cleanly by `curr->next = list1 ? list1 : list2;`. There is no need to write an extra `while` loop to drain remaining nodes.
- [x] **Duplicate Values (`list1->val == list2->val`):**
  - The `<=` comparison chooses `list1`, preserving stable order without requiring additional branching.
- [x] **Stack Dummy vs. Heap Dummy:**
  - Using `ListNode dummy;` instead of `ListNode* dummy = new ListNode(0);` prevents memory leaks and avoids unnecessary dynamic memory allocation overhead.

---

## 5. Clean Code (Optimal Solution: Iterative + Dummy Node)

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
    ListNode* mergeTwoLists(ListNode* list1, ListNode* list2) {
        ListNode dummy;
        ListNode* curr = &dummy;

        while (list1 && list2) {
            if (list1->val <= list2->val) {
                curr->next = list1;
                list1 = list1->next;
            } else {
                curr->next = list2;
                list2 = list2->next;
            }

            curr = curr->next;
        }

        // Attach whichever list has remaining elements
        curr->next = list1 ? list1 : list2;

        return dummy.next;
    }
};
```

---

## 6. Review & Takeaways

### Step-by-Step Dry Run

Given: `list1 = [1, 2, 4]`, `list2 = [1, 3, 4]`

```text
Initial State:
  dummy -> nullptr
  curr points to dummy
  list1: 1 -> 2 -> 4
  list2: 1 -> 3 -> 4

Iteration 1:
  list1->val (1) <= list2->val (1) -> TRUE
  curr->next = list1 (1)
  list1 advances to 2
  curr advances to 1
  Merged: dummy -> 1

Iteration 2:
  list1->val (2) <= list2->val (3) -> TRUE
  curr->next = list1 (2)
  list1 advances to 4
  curr advances to 2
  Merged: dummy -> 1 -> 2

Iteration 3:
  list1->val (4) <= list2->val (3) -> FALSE
  curr->next = list2 (3)
  list2 advances to 4
  curr advances to 3
  Merged: dummy -> 1 -> 2 -> 3

Iteration 4:
  list1->val (4) <= list2->val (4) -> TRUE
  curr->next = list1 (4)
  list1 advances to nullptr
  curr advances to 4
  Merged: dummy -> 1 -> 2 -> 3 -> 4

Loop Ends (list1 is nullptr).
Tail Attachment:
  curr->next = list1 ? list1 : list2 -> attaches list2 (node 4).
  Merged: dummy -> 1 -> 2 -> 3 -> 4 -> 4

Return dummy.next: 1 -> 1 -> 2 -> 3 -> 4 -> 4.
```

---

### The Architectural Pattern

```text
                         Merge Two Sorted Lists
                                    ↓
                         Dummy Node Architecture
                                    ↓
                            ListNode dummy;
                            curr = &dummy;
                                    ↓
                          while (list1 && list2):
                                    ↓
                       list1->val <= list2->val ?
                               /         \
                         YES  /           \  NO
                             ↓             ↓
                    curr->next = list1    curr->next = list2
                    list1 = list1->next   list2 = list2->next
                             \             /
                              \           /
                                    ↓
                            curr = curr->next
                                    ↓
                        curr->next = list1 ? list1 : list2  [O(1) Tail Splice]
                                    ↓
                            return dummy.next
```

* **Next Review Date:** Low priority (standard two-pointer linked list merge pattern mastered).
* **Key Takeaway:** Always use a stack-allocated dummy node to avoid null-head edge cases, re-link existing nodes in-place rather than allocating memory, and splice the remaining tail in a single $O(1)$ assignment once either list is exhausted.
