# 0025. Reverse Nodes in k-Group

- **Problem Link:** https://leetcode.com/problems/reverse-nodes-in-k-group/
- **Difficulty:** `Hard`
- **NeetCode Category:** `Linked List`
- **LeetCode Topics:** `Linked List` / `Recursion`
- **Core Pattern:** `Iterative In-Place Sublist Reversal with Dummy Head & 3-Pointer Window`
- **Last Practiced:** 2026-10-02
- **Proficiency Level:**
  - [x] Level 1: Solved smoothly (< 20 mins, optimal)
  - [ ] Level 2: Struggled / Non-optimal / Edge-case bugs
  - [ ] Level 3: Needed editorial or hints

---

## 1. Pattern Recognition & Triggers

- **Clues in prompt:**
  - Given the `head` of a singly linked list, reverse the nodes of the list $k$ at a time, and return the modified list.
  - $k$ is a positive integer $\le \text{length of the list}$.
  - If the number of nodes is not a multiple of $k$, left-out nodes at the end must remain as-is.
  - You may not alter the values inside nodes; only pointers may be changed.
  - Constraints: $1 \le k \le n \le 5000$.
- **Core intuition:**
  - This problem is the direct bounded generalization of **LeetCode 0206 (Reverse Linked List)**. Instead of reversing the entire list to `nullptr`, we repeatedly reverse subsegments of size $k$ while splicing them seamlessly with preceding and subsequent segments.
  - **4-Phase Group Reversal Architecture:**
    1. **Phase 1 — Lookahead for $k$ Nodes (`find kth`):** Traverse $k$ steps forward starting from `groupPrev`. If fewer than $k$ nodes remain before encountering `nullptr`, the remaining suffix must remain unmodified; return `dummy.next` immediately.
    2. **Phase 2 — Preserve Suffix Boundary (`groupNext`):** Record `groupNext = kth->next` to preserve the entry point to the rest of the list.
    3. **Phase 3 — Bounded 3-Pointer Reversal (`prev = groupNext`):**
       - In whole-list reversal (LC 0206), `prev` is initialized to `nullptr`.
       - Here, initializing `prev = groupNext` right from the start ensures that when the first node of the group (which becomes the new tail) is reversed, its `next` pointer automatically points directly to `groupNext`.
       - Loop terminates when `curr == groupNext`.
    4. **Phase 4 — Reconnect & Advance Stride:**
       - Prior to reversal, `oldGroupHead = groupPrev->next`.
       - After reversal, `kth` is the new head of the reversed group $\implies$ link `groupPrev->next = kth`.
       - Move `groupPrev = oldGroupHead` to position it immediately before the next group.
  - **Why Dummy Node?**
    - Initializing `ListNode dummy(0, head);` eliminates edge cases for updating `head` during the first group's reversal, ensuring every group satisfies the uniform pattern `groupPrev -> [k nodes] -> groupNext`.

---

## 2. Approach & Trade-offs

1. **Approach 1 — Auxiliary Node Array ($O(N)$ time, $O(k)$ or $O(N)$ space):**
   - Collect node pointers in an array of size $k$, rewire pointers or values, and proceed.
   - *Drawback:* Violates the strict $O(1)$ extra space requirement specified in the problem.

2. **Approach 2 — Recursive Divide & Conquer ($O(N)$ time, $O(N/k)$ space):**
   - Check if $k$ nodes exist. If yes, reverse $k$ nodes iteratively and recursively call `head->next = reverseKGroup(groupNext, k)`.
   - *Drawback:* While clean, the recursion consumes $O(N/k)$ call stack frames, which is non-optimal compared to pure iteration.

3. **Approach 3 — Iterative 4-Phase In-Place Reversal (Chosen Optimal Solution):**
   - Maintain a local stack dummy node and a moving pointer `groupPrev`.
   - Perform lookahead to identify `kth`. If not found, break and return.
   - Reverse nodes between `groupPrev->next` and `kth` using 3 pointers with boundary `groupNext`.
   - Reconnect `groupPrev->next = kth` and advance `groupPrev`.
   - *Verdict:* Optimal $O(N)$ time and strict $O(1)$ auxiliary space. Direct extension of the two-pointer/three-pointer linked list pattern, zero dynamic allocations, and zero recursion frames.

---

## 3. Complexity Analysis

- **Time Complexity:** $O(N)$
  - Let $N$ be the total number of nodes in the linked list.
  - Each node is visited at most twice: once during the $k$-step lookahead (`kth = kth->next`), and once during the pointer reversal (`curr->next = prev`).
  - Total operations: at most $2N \in O(N)$.
- **Space Complexity:** $O(1)$
  - Reverses pointers completely in-place.
  - Only uses a few stack pointer variables (`dummy`, `groupPrev`, `kth`, `groupNext`, `curr`, `prev`, `next`).
  - Zero heap allocation and zero recursive call stack memory.

---

## 4. Edge Cases & Gotchas

- [x] **$k = 1$:** Every group of size 1 is verified and reversed in-place trivially; list order remains identical.
- [x] **List Length $< k$:** Lookahead fails on the very first group (`kth` becomes `nullptr`); returns `dummy.next` completely untouched in $O(k)$ time.
- [x] **List Length Exactly Divisible by $k$:** All groups reverse cleanly; the loop terminates when the subsequent lookahead detects `kth == nullptr`.
- [x] **Incomplete Trailing Group ($N \pmod k \neq 0$):** Lookahead reaches `nullptr` midway through the final group; returns `dummy.next` leaving the trailing segment untouched.
- [x] **Subtle Boundary Invariant (`prev = groupNext`):** Starting reversal with `prev = groupNext` instead of `nullptr` eliminates an extra tail-stitching assignment after reversal.

---

## 5. Clean Code (Optimal Solution: Iterative 4-Phase Reversal)

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
    ListNode* reverseKGroup(ListNode* head, int k) {
        ListNode dummy(0, head);
        ListNode* groupPrev = &dummy;

        while (true) {
            // Phase 1: Verify the current group has at least k nodes.
            ListNode* kth = groupPrev;
            for (int i = 0; i < k; ++i) {
                kth = kth->next;
                if (!kth) {
                    return dummy.next;
                }
            }

            // Phase 2: Save the starting node of the subsequent group.
            ListNode* groupNext = kth->next;

            // Phase 3: Reverse the current group in-place.
            // Initializing prev = groupNext ensures the old group head
            // directly connects to groupNext once reversed.
            ListNode* prev = groupNext;
            ListNode* curr = groupPrev->next;
            while (curr != groupNext) {
                ListNode* next = curr->next;
                curr->next = prev;
                prev = curr;
                curr = next;
            }

            // Phase 4: Reconnect preceding segment and advance groupPrev.
            ListNode* oldGroupHead = groupPrev->next;
            groupPrev->next = kth;
            groupPrev = oldGroupHead;
        }
    }
};
```

---

## 6. Review & Takeaways

### Step-by-Step Dry Run

Given: `head = [1, 2, 3, 4, 5]`, $k = 2$.

```text
Initial State:
  dummy -> 1 -> 2 -> 3 -> 4 -> 5 -> nullptr
  groupPrev = dummy

Iteration 1 (Group 1: [1, 2]):
  - Phase 1 (Find kth): kth moves 2 steps: 1 -> 2. kth = 2.
  - Phase 2 (Save next): groupNext = kth->next = 3.
  - Phase 3 (Reverse [1, 2] with prev = 3):
      curr = 1: 1->next = 3, prev = 1, curr = 2
      curr = 2: 2->next = 1, prev = 2, curr = 3 (curr == groupNext, terminates)
      Reversed segment: 2 -> 1 -> 3
  - Phase 4 (Reconnect):
      oldGroupHead = 1
      groupPrev->next = 2  ==>  dummy -> 2 -> 1 -> 3 -> 4 -> 5
      groupPrev = 1

Iteration 2 (Group 2: [3, 4]):
  - Phase 1 (Find kth): kth moves 2 steps from 1: 3 -> 4. kth = 4.
  - Phase 2 (Save next): groupNext = kth->next = 5.
  - Phase 3 (Reverse [3, 4] with prev = 5):
      Reversed segment: 4 -> 3 -> 5
  - Phase 4 (Reconnect):
      oldGroupHead = 3
      groupPrev->next = 4  ==>  dummy -> 2 -> 1 -> 4 -> 3 -> 5
      groupPrev = 3

Iteration 3 (Group 3: [5]):
  - Phase 1 (Find kth): kth moves 1 step to 5, step 2 reaches nullptr.
  - kth == nullptr  ==>  Return dummy.next immediately.

Final Result: 2 -> 1 -> 4 -> 3 -> 5.
```

---

### The Architectural Mental Model

```text
                        Reverse Nodes in k-Group
                                   ↓
                       ListNode dummy(0, head);
                           groupPrev = &dummy;
                                   ↓
                             while (true):
                                   ↓
                   Phase 1: kth = groupPrev (advance k times)
                          kth == nullptr ?
                              /        \
                        YES  /          \  NO
                            ↓            ↓
                     Return dummy.next   Phase 2: groupNext = kth->next
                                         Phase 3: prev = groupNext, curr = groupPrev->next
                                                  while (curr != groupNext):
                                                      reverse pointers
                                         Phase 4: oldGroupHead = groupPrev->next
                                                  groupPrev->next = kth
                                                  groupPrev = oldGroupHead
```

* **Next Review Date:** As needed / TBD
* **Key Takeaway:** To reverse sublists cleanly in $O(1)$ space, always initialize `prev = groupNext` before reversing so the new tail stitches directly to the remaining list, and verify $k$ nodes upfront to prevent modifying incomplete trailing suffixes.
