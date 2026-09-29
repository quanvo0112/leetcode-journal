# 0019. Remove Nth Node From End of List

- **Problem Link:** https://leetcode.com/problems/remove-nth-node-from-end-of-list/
- **Difficulty:** `Medium`
- **NeetCode Category:** `Linked List`
- **LeetCode Topics:** `Linked List` / `Two Pointers`
- **Core Pattern:** `Two Pointers with Fixed Offset (Gap = n + 1) + Dummy Head Node`
- **Last Practiced:** 2026-09-29
- **Proficiency Level:**
  - [x] Level 1: Solved smoothly (< 20 mins, optimal)
  - [ ] Level 2: Struggled / Non-optimal / Edge-case bugs
  - [ ] Level 3: Needed editorial or hints

---

## 1. Pattern Recognition & Triggers

- **Clues in prompt:**
  - Given the `head` of a linked list, remove the $n$-th node from the end of the list and return its head.
  - Follow-up challenge: Can you accomplish this in a **single pass**?
- **Core intuition:**
  - Singly linked lists can only be traversed forward. To delete a node, we must position our pointer at its **predecessor** (`prev->next = prev->next->next`).
  - The $n$-th node from the end is at offset $L - n$ from the beginning (where $L$ is the total length). Its predecessor is at index $L - n - 1$.
  - Instead of a two-pass approach (counting $L$ then traversing $L - n$), we can create a **fixed sliding window** of two pointers:
    - If `fast` starts $n + 1$ nodes ahead of `slow`, then when `fast` traverses past the end of the list (`fast == nullptr`), `slow` will naturally stop at the node immediately before the target.
  - Prepending a stack-allocated **dummy node** (`ListNode dummy(0, head);`) unifies edge-case handling, allowing the deletion of the `head` node without dedicated conditional branches.

---

## 2. Approach & Trade-offs

1. **Approach 1 — Two-Pass Length Calculation ($O(N)$ time, $O(1)$ space):**
   - Traverse the list once to compute total length $L$.
   - Traverse a second time to index $L - n - 1$, then delete the next node.
   - *Drawback:* Requires two full passes over the list, failing the one-pass optimization goal.

2. **Approach 2 — Auxiliary Vector of Pointers ($O(N)$ time, $O(N)$ space):**
   - Store all node pointers in a `std::vector<ListNode*>`.
   - Access the target node directly at `vec[size - n]`.
   - *Drawback:* Wastes $O(N)$ auxiliary memory when two pointers can achieve the same result in $O(1)$ space.

3. **Approach 3 — Dummy Node + Two Pointers with $(n + 1)$ Offset (Chosen Optimal Solution):**
   - Allocate `ListNode dummy(0, head);` on the local stack. Initialize `slow = &dummy` and `fast = &dummy`.
   - Advance `fast` forward by $n + 1$ steps.
   - Advance both `slow` and `fast` in lockstep until `fast == nullptr`.
   - `slow` is now positioned at the predecessor of the node to remove.
   - Preserve `ListNode* toDelete = slow->next;`, update `slow->next = slow->next->next;`, and deallocate via `delete toDelete;`.
   - Return `dummy.next`.
   - *Verdict:* Optimal single-pass $O(N)$ time, $O(1)$ auxiliary space, clean C++ memory management, and uniform handling for all node positions.

---

## 3. Complexity Analysis

- **Time Complexity:** $O(N)$
  - `fast` traverses each node in the list of length $N$ at most once. Both pointers advance in a single pass.
- **Space Complexity:** $O(1)$
  - Operates strictly in-place using only a local stack-allocated dummy node and two auxiliary pointers (`slow`, `fast`).

---

## 4. Edge Cases & Gotchas

- [x] **Deleting the Head Node ($n = L$):**
  - When deleting `head`, the $n + 1$ lead moves `fast` completely past the list to `nullptr`. The subsequent `while` loop never executes. `slow` remains parked at `&dummy`, so `slow->next` is `head`. Rewiring updates `dummy.next = head->next`, seamlessly removing the original head without special-case logic.
- [x] **Single-Node List ($L = 1, n = 1$):**
  - `dummy -> 1 -> nullptr`. `fast` advances 2 steps to `nullptr`. `slow` remains at `dummy`. `slow->next` is deleted and `dummy.next` becomes `nullptr`.
- [x] **Deleting the Tail Node ($n = 1$):**
  - `fast` advances 2 steps ahead. When `fast == nullptr`, `slow` rests at the penultimate node. `slow->next` is rewired to `nullptr`.
- [x] **Why the Offset Must Be $n + 1$, Not $n$:**
  - An offset of $n$ would place `slow` directly on the target node itself. In a singly linked list, a node cannot delete itself without its predecessor. Moving $n + 1$ steps ensures `slow` stops on the predecessor.
- [x] **Explicit Memory Deallocation:**
  - Caching `ListNode* toDelete = slow->next;` prior to pointer rewiring allows invoking `delete toDelete;`, preventing memory leaks in idiomatic C++.

---

## 5. Clean Code (Optimal Solution: Dummy Node + Two Pointers)

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
    ListNode* removeNthFromEnd(ListNode* head, int n) {
        ListNode dummy(0, head);

        ListNode* slow = &dummy;
        ListNode* fast = &dummy;

        // Keep fast n + 1 nodes ahead of slow
        for (int i = 0; i <= n; ++i) {
            fast = fast->next;
        }

        // Move both pointers until fast reaches the end
        while (fast != nullptr) {
            slow = slow->next;
            fast = fast->next;
        }

        // slow->next is the node to remove
        ListNode* toDelete = slow->next;
        slow->next = slow->next->next;

        delete toDelete;

        return dummy.next;
    }
};
```

---

## 6. Review & Takeaways

### Step-by-Step Dry Run

Given: `1 -> 2 -> 3 -> 4 -> 5`, $n = 2$ (Target to delete: node `4`)

```text
Initial State:
  dummy -> 1 -> 2 -> 3 -> 4 -> 5 -> nullptr
  ^
  slow, fast

Advance fast by n + 1 = 3 steps:
  Step 0: fast = 1
  Step 1: fast = 2
  Step 2: fast = 3

  dummy -> 1 -> 2 -> 3 -> 4 -> 5 -> nullptr
    ^                ^
   slow             fast

Lockstep Movement:
  Iteration 1: slow = 1, fast = 4
  Iteration 2: slow = 2, fast = 5
  Iteration 3: slow = 3, fast = nullptr (Loop ends)

Result of traversal:
  slow is at node 3 (predecessor)
  toDelete = slow->next = node 4

Pointer Rewire:
  slow->next = slow->next->next (3 -> 5)
  delete node 4

Return dummy.next: 1 -> 2 -> 3 -> 5 -> nullptr.
```

---

### The Architectural Pattern

```text
               Remove Nth Node From End (One-Pass)
                                ↓
                      ListNode dummy(0, head);
                     slow = &dummy, fast = &dummy;
                                ↓
               Advance fast by n + 1 steps (Offset Window)
                                ↓
                  while (fast != nullptr):
                     slow = slow->next;
                     fast = fast->next;
                                ↓
                fast is null ──> slow is predecessor
                                ↓
                  toDelete = slow->next;
                  slow->next = slow->next->next;
                  delete toDelete;
                                ↓
                       return dummy.next;
```

* **Next Review Date:** Low priority (two-pointer fixed window on linked list pattern mastered).
* **Key Takeaway:** To delete the $n$-th node from the end in one pass, offset `fast` by $n + 1$ steps ahead of `slow` starting from a `dummy` node. When `fast` reaches `nullptr`, `slow` lands precisely on the node before the target.
