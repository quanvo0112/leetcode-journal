# 0023. Merge k Sorted Lists

- **Problem Link:** https://leetcode.com/problems/merge-k-sorted-lists/
- **Difficulty:** `Hard`
- **NeetCode Category:** `Linked List`
- **LeetCode Topics:** `Linked List` / `Divide and Conquer` / `Heap (Priority Queue)` / `Merge Sort`
- **Core Pattern:** `Iterative Divide & Conquer / Bottom-Up Pairwise Merge`
- **Last Practiced:** 2026-10-02
- **Proficiency Level:**
  - [x] Level 1: Solved smoothly (< 20 mins, optimal)
  - [ ] Level 2: Struggled / Non-optimal / Edge-case bugs
  - [ ] Level 3: Needed editorial or hints

---

## 1. Pattern Recognition & Triggers

- **Clues in prompt:**
  - You are given an array of $k$ linked lists `lists`, where each linked list is sorted in ascending order.
  - Merge all the linked lists into one sorted linked list and return its head.
  - Constraints: $k \le 10^4$, total nodes $\sum \text{nodes} \le 10^4$.
- **Core intuition:**
  - This problem is the direct multi-way scaling of **LeetCode 0021 (Merge Two Sorted Lists)** from 2 lists to $k$ lists.
  - **Why not linear sequential merging?** Merging list 0 with list 1, then merging the accumulated result with list 2, list 3, ..., causes earlier nodes to be traversed repeatedly up to $k$ times, degrading runtime to $O(k \cdot N)$.
  - **Why Divide & Conquer?** By pairing lists up and merging them two-by-two, every round halves the number of remaining lists ($\lceil \log_2 k \rceil$ levels). In every level, all $N$ nodes across all lists are traversed and spliced exactly once in $O(N)$ time. The overall runtime drops from $O(k \cdot N)$ to optimal $O(N \log k)$.
  - **Bottom-Up Iteration (`interval *= 2`) vs. Top-Down Recursion:**
    - Standard recursive Divide & Conquer introduces $O(\log k)$ call stack frames.
    - An iterative bottom-up approach doubling the stride interval (`interval = 1, 2, 4, 8, ...`) updates the input `vector<ListNode*>& lists` in-place, eliminating all recursion overhead and achieving true $O(1)$ auxiliary space.
  - **In-Place Node Splicing:** No new node memory needs to be allocated. We reuse the $O(1)$ space pointer-rewiring helper from LeetCode 0021.

---

## 2. Approach & Trade-offs

1. **Approach 1 — Sequential Accumulation ($O(k \cdot N)$ time, $O(1)$ space):**
   - Accumulate lists one-by-one: `merged = mergeTwoLists(merged, lists[i])`.
   - *Drawback:* Severe performance bottleneck. For $k = 10^4$, repeatedly scanning the growing list results in quadratic-like node visits, resulting in Time Limit Exceeded (TLE).

2. **Approach 2 — Min-Heap / Priority Queue ($O(N \log k)$ time, $O(k)$ space):**
   - Push the head of each non-empty list into a min-priority queue of size $k$. Repeatedly extract the minimum node, append it to the merged list, and push its `next` pointer into the heap.
   - *Drawback:* Optimal time, but requires maintaining an external container allocating $O(k)$ auxiliary heap memory and comparator wrappers.

3. **Approach 3 — Recursive Divide & Conquer ($O(N \log k)$ time, $O(\log k)$ space):**
   - Recursively split the array range `[left, right]`, merge each half, and combine via `mergeTwoLists`.
   - *Drawback:* Incurs $O(\log k)$ recursive call stack depth.

4. **Approach 4 — Iterative Bottom-Up Pairwise Merge (Chosen Optimal Solution):**
   - Initialize stride `interval = 1`.
   - In each level, iterate index `i` from `0` to `n - interval` with step `interval * 2`:
     - Merge `lists[i]` and `lists[i + interval]` using `mergeTwoLists`.
     - Overwrite `lists[i]` with the merged result.
   - Double `interval *= 2` after each pass.
   - Stop when `interval >= n`. The complete merged list resides at `lists[0]`.
   - *Verdict:* Optimal $O(N \log k)$ time and strict $O(1)$ auxiliary space. Zero heap memory allocations, zero call stack frames, and direct reuse of the two-pointer linked list pattern from LeetCode 0021.

---

## 3. Complexity Analysis

- **Time Complexity:** $O(N \log k)$
  - Let $k$ be the total number of lists (`lists.size()`) and $N$ be the total number of nodes across all lists.
  - In each outer iteration (round), lists are merged in pairs. Every node in the current round is visited and spliced at most once during the two-pointer linear merge, taking $O(N)$ total operations per round.
  - The number of remaining lists is halved after each round (`interval` doubles: $1, 2, 4, 8, \dots$), requiring exactly $\lceil \log_2 k \rceil$ outer rounds.
  - Total Time: $O(N \times \log_2 k) = O(N \log k)$.
- **Space Complexity:** $O(1)$
  - Operates strictly in-place by reconnecting existing `next` pointers within `lists`.
  - The helper `mergeTwoLists` allocates a single local stack dummy node.
  - No min-heap, no auxiliary lists, and no recursion stack frames ($O(1)$ vs. $O(\log k)$ recursion / $O(k)$ priority queue).

---

## 4. Edge Cases & Gotchas

- [x] **Empty Outer Vector (`lists = []`):**
  - Handled by initial check: `if (n == 0) return nullptr;`.
- [x] **Vector Containing Single List (`lists = [[1, 2, 3]]`):**
  - Outer loop `interval < 1` does not execute; returns `lists[0]` directly in $O(1)$ time.
- [x] **Vector of Empty Lists (`lists = [[], []]`):**
  - `mergeTwoLists(nullptr, nullptr)` returns `nullptr`. Result is `nullptr`.
- [x] **Odd Number of Lists in a Round:**
  - Handled seamlessly by the loop bound `i + interval < n`. An unpaired list at the tail is carried over untouched to be merged in the subsequent round.
- [x] **Zero Memory Allocation:**
  - Using existing pointers rather than `new ListNode()` guarantees zero memory leaks and avoids dynamic allocation overhead.

---

## 5. Clean Code (Optimal Solution: Iterative Divide & Conquer)

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
private:
    ListNode* mergeTwoLists(ListNode* l1, ListNode* l2) {
        ListNode dummy;
        ListNode* curr = &dummy;

        while (l1 && l2) {
            if (l1->val <= l2->val) {
                curr->next = l1;
                l1 = l1->next;
            } else {
                curr->next = l2;
                l2 = l2->next;
            }
            curr = curr->next;
        }

        curr->next = l1 ? l1 : l2;
        return dummy.next;
    }

public:
    ListNode* mergeKLists(vector<ListNode*>& lists) {
        int n = lists.size();
        if (n == 0) {
            return nullptr;
        }

        // Bottom-up pairwise merge (Iterative Divide & Conquer)
        // Round 1: merge (0, 1), (2, 3), (4, 5)...
        // Round 2: merge (0, 2), (4, 6)...
        // Round 3: merge (0, 4)...
        // Repeat until only one list remains at index 0.
        for (int interval = 1; interval < n; interval *= 2) {
            for (int i = 0; i + interval < n; i += interval * 2) {
                lists[i] = mergeTwoLists(lists[i], lists[i + interval]);
            }
        }

        return lists[0];
    }
};
```

---

## 6. Review & Takeaways

### Step-by-Step Dry Run

Given: `lists = [[1, 4, 5], [1, 3, 4], [2, 6]]`, $n = 3$.

```text
Initial State:
  lists[0] = 1 -> 4 -> 5
  lists[1] = 1 -> 3 -> 4
  lists[2] = 2 -> 6

Round 1 (interval = 1):
  - i = 0, i + interval = 1 < 3:
    mergeTwoLists(lists[0], lists[1])
    lists[0] = 1 -> 1 -> 3 -> 4 -> 4 -> 5
  - i advances to 0 + (1 * 2) = 2.
    i + interval = 2 + 1 = 3 (not < 3, loop terminates).
    lists[2] = 2 -> 6 remains untouched.

Round 2 (interval = 2):
  - i = 0, i + interval = 2 < 3:
    mergeTwoLists(lists[0], lists[2])
    lists[0] = 1 -> 1 -> 2 -> 3 -> 4 -> 4 -> 5 -> 6
  - i advances to 0 + (2 * 2) = 4 (not < 3, loop terminates).

Round 3 (interval = 4):
  - interval = 4 >= n (3), outer loop terminates.

Return lists[0]: 1 -> 1 -> 2 -> 3 -> 4 -> 4 -> 5 -> 6.
```

---

### The Architectural Mental Model

```text
                           Merge k Sorted Lists
                                    ↓
                         Divide & Conquer Paradigm
                                    ↓
                       Bottom-Up Iterative Stride
                 for (int interval = 1; interval < n; interval *= 2)
                                    ↓
                   Pairwise Merge Adjacent Active Slots:
                 lists[i] = mergeTwoLists(lists[i], lists[i + interval])
                                    ↓
                  L0       L1       L2       L3       L4       L5
                   \      /          \      /          \      /
                    \    /            \    /            \    /   [interval = 1]
                     L0,1              L2,3              L4,5
                       \                /                 /
                        \              /                 /     [interval = 2]
                             L0,1,2,3                  L4,5
                                 \                      /
                                  \                    /       [interval = 4]
                                     L0,1,2,3,4,5
                                          ↓
                                    Return lists[0]
                         Time: O(N log k) | Space: O(1)
```

* **Next Review Date:** As needed / TBD
* **Key Takeaway:** Merge $k$ sorted lists by pairing them bottom-up with doubling stride intervals (`interval *= 2`); this matches Merge Sort's reduction tree, cutting the runtime to $O(N \log k)$ while keeping auxiliary memory strictly $O(1)$ by directly reusing the iterative two-pointer splice helper.
