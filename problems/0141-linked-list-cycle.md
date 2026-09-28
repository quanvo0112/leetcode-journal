# 0141. Linked List Cycle

- **Problem Link:** https://leetcode.com/problems/linked-list-cycle/
- **Difficulty:** `Easy`
- **NeetCode Category:** `Linked List`
- **LeetCode Topics:** `Hash Table` / `Linked List` / `Two Pointers`
- **Core Pattern:** `Floyd's Cycle Detection (Fast & Slow Pointers / Tortoise and Hare)`
- **Last Practiced:** 2026-09-28
- **Proficiency Level:**
  - [x] Level 1: Solved smoothly (< 20 mins, optimal)
  - [ ] Level 2: Struggled / Non-optimal / Edge-case bugs
  - [ ] Level 3: Needed editorial or hints

---

## 1. Pattern Recognition & Triggers

- **Clues in prompt:**
  - Given `head`, the head of a linked list, determine if the linked list has a cycle in it.
  - Return `true` if there is a cycle, otherwise return `false`.
  - Follow-up challenge: Can you solve it using $O(1)$ (i.e. constant) memory?
- **Core intuition:**
  - In a standard acyclic list, traversing forward eventually reaches `nullptr`.
  - In a cyclic list, a pointer loops endlessly without terminating.
  - If two runners run along a track at different speeds:
    - `slow` takes **1 step** per iteration.
    - `fast` takes **2 steps** per iteration.
  - **Acyclic Track:** `fast` reaches the finish line (`nullptr`) first.
  - **Cyclic Track:** Once both runners enter the closed loop, `fast` gains $2 - 1 = 1$ step on `slow` in every single iteration. Because the cycle has a finite integer circumference, `fast` is guaranteed to catch up and collide with `slow` (`slow == fast`) without skipping over it.

---

## 2. Approach & Trade-offs

1. **Approach 1 — Hash Set of Visited Pointers ($O(N)$ time, $O(N)$ space):**
   - Traverse the list and insert each node address into an `std::unordered_set<ListNode*>`.
   - If a node address already exists in the set, a cycle is detected. If `nullptr` is hit, return `false`.
   - *Drawback:* Consumes $O(N)$ auxiliary memory and incurs hash set collision/allocation overhead, violating the $O(1)$ memory goal.

2. **Approach 2 — Destructive Node Mutation ($O(N)$ time, $O(1)$ space):**
   - Overwrite visited node values with an impossible sentinel value (e.g. `1000000`) or point every visited node's `next` to a shared dummy sentinel.
   - *Drawback:* Violates data integrity by destructively modifying the caller's data structure, which is unsafe in multi-threaded or read-only production environments.

3. **Approach 3 — Floyd's Tortoise and Hare (Chosen Optimal Solution):**
   - Initialize `slow = head` and `fast = head`.
   - Advance while `fast != nullptr && fast->next != nullptr`:
     - `slow = slow->next;`
     - `fast = fast->next->next;`
     - If `slow == fast`, collision confirmed $\implies$ return `true`.
   - If the loop exits because `fast` or `fast->next` is `nullptr`, return `false`.
   - *Verdict:* Optimal $O(N)$ time and $O(1)$ auxiliary space. Non-destructive, cache-efficient, and the gold standard for cycle detection.

---

## 3. Complexity Analysis

- **Time Complexity:** $O(N)$
  - **Case 1 (No Cycle):** `fast` advances 2 nodes at a time and reaches `nullptr` in $\lceil N / 2 \rceil$ iterations $\implies O(N)$.
  - **Case 2 (Cycle Exists):** Let $K$ be the acyclic prefix length and $C$ be the cycle length ($K + C \le N$). `slow` enters the cycle after $K$ steps. Within the cycle, the gap between `fast` and `slow` is at most $C - 1$. Because the relative speed is $2 - 1 = 1$ step per tick, `fast` catches `slow` in at most $C$ iterations. Total iterations $\le K + C \le N \implies O(N)$.
- **Space Complexity:** $O(1)$
  - Uses only two pointer references (`slow`, `fast`). No auxiliary data structures or heap allocations.

---

## 4. Edge Cases & Gotchas

- [x] **Empty List (`head == nullptr`):**
  - `while (fast != nullptr && ...)` fails immediately on the initial check; returns `false`.
- [x] **Single-Node List Without Cycle (`head->next == nullptr`):**
  - `fast->next != nullptr` evaluates to false immediately; returns `false`.
- [x] **Single-Node Self-Loop (`head->next == head`):**
  - Iteration 1: `slow` advances to `head`, `fast` advances to `head->next->next = head`. `slow == fast` triggers and returns `true`.
- [x] **Two-Node Cycle (`A -> B -> A`):**
  - Correctly detected within 2 iterations without null dereferencing.
- [x] **Null Pointer Dereference Protection:**
  - Checking both `fast != nullptr` and `fast->next != nullptr` is mandatory before evaluating `fast->next->next`.

---

## 5. Clean Code (Optimal Solution: Floyd's Cycle Detection)

```cpp
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode(int x) : val(x), next(NULL) {}
 * };
 */
class Solution {
public:
    bool hasCycle(ListNode* head) {
        ListNode* slow = head;
        ListNode* fast = head;

        // Fast moves 2 steps, slow moves 1 step
        while (fast != nullptr && fast->next != nullptr) {
            slow = slow->next;
            fast = fast->next->next;

            // Pointers collided inside a cycle
            if (slow == fast) {
                return true;
            }
        }

        // Fast reached the end of the list (acyclic)
        return false;
    }
};
```

---

## 6. Review & Takeaways

### Step-by-Step Dry Run

Given: `3 -> 2 -> 0 -> -4` where `-4` links back to `2` (Cycle: `2 -> 0 -> -4 -> 2`)

```text
Initial State:
  slow = 3 (index 0)
  fast = 3 (index 0)

Iteration 1:
  slow = slow->next = 2 (index 1)
  fast = fast->next->next = 0 (index 2)
  slow == fast ? 2 == 0 -> FALSE

Iteration 2:
  slow = slow->next = 0 (index 2)
  fast = fast->next->next = 2 (index 1, wrapped around)
  slow == fast ? 0 == 2 -> FALSE

Iteration 3:
  slow = slow->next = -4 (index 3)
  fast = fast->next->next = -4 (index 3, wrapped around)
  slow == fast ? -4 == -4 -> TRUE! Collision detected.

Return true.
```

---

### The Architectural Pattern

```text
                     Floyd's Cycle Detection
                                ↓
                      Two Pointers Initialization
                        slow = head, fast = head
                                ↓
                  while (fast && fast->next):
                                ↓
                     ┌───────────────────────┐
                     │ slow = slow->next     │ (+1 step)
                     │ fast = fast->next->next│ (+2 steps)
                     └───────────────────────┘
                                ↓
                          slow == fast ?
                             /     \
                       YES  /       \  NO
                           ↓         ↓
                      return true   Continue loop
                                ↓
                   fast reached nullptr ──> return false
```

* **Next Review Date:** Low priority (benchmark fast & slow pointer cycle detection mastered).
* **Key Takeaway:** Use two pointers moving at speeds of 1 and 2 (`slow = slow->next`, `fast = fast->next->next`). Guard the loop with `while (fast && fast->next)` to safely achieve $O(N)$ time and $O(1)$ space without hash sets or destructive node mutations.
