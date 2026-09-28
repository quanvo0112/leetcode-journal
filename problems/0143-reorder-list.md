# 0143. Reorder List

- **Problem Link:** https://leetcode.com/problems/reorder-list/
- **Difficulty:** `Medium`
- **NeetCode Category:** `Linked List`
- **LeetCode Topics:** `Linked List` / `Two Pointers` / `Stack` / `Recursion`
- **Core Pattern:** `Find Middle (Fast/Slow Pointers) + Reverse Second Half (In-Place 3 Pointers) + Alternating Merge`
- **Last Practiced:** 2026-09-28
- **Proficiency Level:**
  - [x] Level 1: Solved smoothly (< 20 mins, optimal)
  - [ ] Level 2: Struggled / Non-optimal / Edge-case bugs
  - [ ] Level 3: Needed editorial or hints

---

## 1. Pattern Recognition & Triggers

- **Clues in prompt:**
  - Given the head of a singly linked list $L_0 \to L_1 \to \dots \to L_{n-1} \to L_n$.
  - Reorder it into the interleaved form: $L_0 \to L_n \to L_1 \to L_{n-1} \to L_2 \to L_{n-2} \to \dots$.
  - Must be performed in-place without altering node values (pure pointer manipulation).
- **Core intuition:**
  - A singly linked list only possesses forward pointers (`next`), meaning we cannot traverse backward from the tail without external storage.
  - The interleaved sequence alternates taking one node from the front and one node from the back.
  - If we split the list into two halves, **reversing the second half** makes the original tail the head of the second sublist.
  - Once the second half is reversed, the problem reduces to alternately splicing nodes between two forward-moving lists:
    1. **Find Middle:** Locate the split boundary using Fast & Slow pointers.
    2. **Reverse Second Half:** Invert pointers of the second half in-place using the 3-pointer pattern.
    3. **Alternating Merge:** Weave the two halves together by updating `next` links sequentially.

---

## 2. Approach & Trade-offs

1. **Approach 1 — Array / Vector of Node Pointers ($O(N)$ time, $O(N)$ space):**
   - Store all `ListNode*` in a dynamic vector. Use two index pointers (`left = 0`, `right = n - 1`) to alternate links.
   - *Drawback:* Consumes $O(N)$ extra heap memory, failing the optimal $O(1)$ auxiliary space standard expected in technical interviews.

2. **Approach 2 — Recursive Tail Traversal ($O(N)$ time, $O(N)$ space):**
   - Recurse to the tail while passing an advance pointer from the head. Unwind the stack while rewiring links.
   - *Drawback:* Uses $O(N)$ call stack frames, exposing the solution to potential stack overflow on deep lists ($N \ge 10^4$).

3. **Approach 3 — Find Middle + Reverse Second Half + Alternating Merge (Chosen Optimal Solution):**
   - **Step 1 (Find Middle):** Advance `slow` by 1 and `fast` by 2 using condition `while (fast->next && fast->next->next)`. For odd lengths, `slow` lands on the exact middle node; for even lengths, `slow` lands on the first of the two middle nodes.
   - **Step 2 (Reverse Second Half):** Split the list by capturing `second = slow->next` and severing `slow->next = nullptr`. Reverse `second` in-place using standard 3 pointers (`prev`, `second`, `next`).
   - **Step 3 (Alternating Merge):** Maintain `first = head` and `second = prev`. While `second` is non-null, temporarily cache `firstNext = first->next` and `secondNext = second->next`, rewire `first->next = second` and `second->next = firstNext`, then step both forward.
   - *Verdict:* Optimal $O(N)$ time and $O(1)$ auxiliary space. Zero heap allocations, modular, and composed entirely of standard linked list primitives.

---

## 3. Complexity Analysis

- **Time Complexity:** $O(N)$
  - Finding the middle takes $N / 2$ steps $\implies O(N)$.
  - Reversing the second half takes $N / 2$ pointer flips $\implies O(N)$.
  - Alternating merge weaves $N$ nodes in $N / 2$ steps $\implies O(N)$.
  - Total time: $O(N) + O(N) + O(N) = O(N)$.
- **Space Complexity:** $O(1)$
  - Operates strictly in-place using a few primitive pointer variables (`slow`, `fast`, `prev`, `curr`, `firstNext`, `secondNext`). No additional nodes or containers are allocated.

---

## 4. Edge Cases & Gotchas

- [x] **Small Lists ($N \le 2$):**
  - If `!head || !head->next`, returns immediately. A list with 2 nodes (`1 -> 2`) bypasses the loop, reverses node 2 to itself, and merges into `1 -> 2` unchanged.
- [x] **Odd vs. Even Length Parity:**
  - Using `while (fast->next && fast->next->next)` ensures that for odd lengths (`1 -> 2 -> 3 -> 4 -> 5`), `slow` stops at `3`. The first half has 3 nodes (`1 -> 2 -> 3`) and the second half has 2 nodes (`5 -> 4`). Because the loop terminates when `second == nullptr`, the extra middle node (`3`) naturally remains at the end without extra checks.
- [x] **Severing the List Split (`slow->next = nullptr`):**
  - You must sever the connection between the two halves before reversing. Omitting `slow->next = nullptr;` creates an infinite circular reference during the alternating merge.
- [x] **Pointer Severance Protection:**
  - During the merge step, both `first->next` and `second->next` must be stored into temporary variables (`firstNext`, `secondNext`) before redirecting links.

---

## 5. Clean Code (Optimal Solution: 3-Step In-Place Algorithm)

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
    void reorderList(ListNode* head) {
        if (!head || !head->next) {
            return;
        }

        // 1. Find the middle of the list
        ListNode* slow = head;
        ListNode* fast = head;

        while (fast->next && fast->next->next) {
            slow = slow->next;
            fast = fast->next->next;
        }

        // 2. Reverse the second half
        ListNode* second = slow->next;
        slow->next = nullptr; // Sever connection between halves

        ListNode* prev = nullptr;

        while (second) {
            ListNode* next = second->next;
            second->next = prev;
            prev = second;
            second = next;
        }

        second = prev; // New head of reversed second half

        // 3. Merge two halves alternately
        ListNode* first = head;

        while (second) {
            ListNode* firstNext = first->next;
            ListNode* secondNext = second->next;

            first->next = second;
            second->next = firstNext;

            first = firstNext;
            second = secondNext;
        }
    }
};
```

---

## 6. Review & Takeaways

### Step-by-Step Dry Run

Given: `1 -> 2 -> 3 -> 4 -> 5`

#### Step 1: Find Middle
- `slow` and `fast` start at `1`.
- Iteration 1: `slow = 2`, `fast = 3`.
- Iteration 2: `slow = 3`, `fast = 5`. `fast->next` is `nullptr` $\implies$ loop terminates.
- `slow` is at node `3`.
- Sever link: `second = slow->next` (`4`), `slow->next = nullptr`.
- Two lists: `first = 1 -> 2 -> 3 -> nullptr`, `second = 4 -> 5 -> nullptr`.

#### Step 2: Reverse Second Half (`4 -> 5`)
- Reverse pointers: `5 -> 4 -> nullptr`.
- `second = 5`.
- Two lists: `first = 1 -> 2 -> 3`, `second = 5 -> 4`.

#### Step 3: Alternating Merge
- **Iteration 1:**
  - `firstNext = 2`, `secondNext = 4`.
  - `first->next = 5`, `second->next = 2`.
  - Reordered prefix: `1 -> 5 -> 2 -> 3`.
  - Advance: `first = 2`, `second = 4`.
- **Iteration 2:**
  - `firstNext = 3`, `secondNext = nullptr`.
  - `first->next = 4`, `second->next = 3`.
  - Reordered prefix: `1 -> 5 -> 2 -> 4 -> 3`.
  - Advance: `first = 3`, `second = nullptr`.
- Loop terminates (`second == nullptr`).
- Final Result: `1 -> 5 -> 2 -> 4 -> 3`.

---

### The Architectural Pattern

```text
                           Reorder List (LC 143)
                                     ↓
             ┌───────────────────────┼───────────────────────┐
             ↓                       ↓                       ↓
      1. Find Middle          2. Reverse Half         3. Weave Merge
     (Fast/Slow LC 141)        (3 Pointers LC 206)      (Two Lists LC 21)
             ↓                       ↓                       ↓
    slow advances by 1      reverse pointers from    first->next = second
    fast advances by 2      mid->next to tail       second->next = firstNext
             ↓                       ↓                       ↓
    slow->next = nullptr      second = prev          advance both pointers
```

* **Next Review Date:** Low priority (composite linked list master pattern internalized).
* **Key Takeaway:** Reorder List is the quintessential composite problem: **Find Middle (Fast/Slow)** $\to$ **Reverse Second Half (3 Pointers)** $\to$ **Interleaved Merge**. Mastering these three independent building blocks solves the problem in $O(N)$ time and $O(1)$ space without vector buffers.
