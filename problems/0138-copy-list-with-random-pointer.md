# 0138. Copy List with Random Pointer

- **Problem Link:** https://leetcode.com/problems/copy-list-with-random-pointer/
- **Difficulty:** `Medium`
- **NeetCode Category:** `Linked List`
- **LeetCode Topics:** `Hash Table` / `Linked List`
- **Core Pattern:** `Interweaving Nodes (3-Pass In-Place Mapping: Clone, Link Random, Decouple)`
- **Last Practiced:** 2026-09-29
- **Proficiency Level:**
  - [x] Level 1: Solved smoothly (< 20 mins, optimal)
  - [ ] Level 2: Struggled / Non-optimal / Edge-case bugs
  - [ ] Level 3: Needed editorial or hints

---

## 1. Pattern Recognition & Triggers

- **Clues in prompt:**
  - A linked list of length $n$ is given where each node contains an extra `random` pointer that can point to any node in the list, or `null`.
  - Construct a **deep copy** of the list.
  - None of the pointers in the new list may point to nodes in the original list.
- **Core intuition:**
  - In a standard singly linked list, nodes can be duplicated sequentially in a single pass.
  - However, `random` pointers can point arbitrarily forward, backward, to self, or to `nullptr`.
  - To set `copy->random`, we must know the exact clone corresponding to `original->random`.
  - The naive approach maps $\text{original} \to \text{clone}$ using an `unordered_map<Node*, Node*>`, but requires $O(N)$ extra space.
  - **The Interweaving Insight:** We can use the linked list itself as the hash map by inserting each copied node immediately after its original counterpart:
    $$A \to a \to B \to b \to C \to c$$
  - In this interleaved state, the clone of any node $X$ is always uniquely reachable at $X\text{->next}$.
  - Therefore, if $A\text{->random} = C$, then the cloned random target is simply $A\text{->random->next} = c$.
  - After assigning all random pointers in pass 2, pass 3 cleanly unweaves the two lists back into their separate original and copied structures.

---

## 2. Approach & Trade-offs

1. **Approach 1 — Hash Map Mapping (`unordered_map<Node*, Node*>`) ($O(N)$ time, $O(N)$ space):**
   - First pass: create all cloned nodes and store pairs in `map[curr] = new Node(curr->val)`.
   - Second pass: wire `map[curr]->next = map[curr->next]` and `map[curr]->random = map[curr->random]`.
   - *Drawback:* Consumes $O(N)$ auxiliary heap memory for the hash table, and hash map lookups add runtime overhead.

2. **Approach 2 — Interweaving / Interleaving Nodes (Chosen Optimal Solution):**
   - **Pass 1 (Clone & Insert):** For every original node `curr`, allocate `Node* copy = new Node(curr->val)`. Splice `copy` immediately after `curr`: `copy->next = curr->next; curr->next = copy;`.
   - **Pass 2 (Wire Random Pointers):** For each original node `curr`, if `curr->random != nullptr`, wire `curr->next->random = curr->random->next`.
   - **Pass 3 (Decouple Lists):** Restore original `curr->next = copy->next;` and connect copied list `copy->next = copy->next ? copy->next->next : nullptr;`.
   - *Verdict:* Optimal $O(N)$ time and $O(1)$ auxiliary space (excluding the output list). Highly interview-friendly and showcases advanced pointer manipulation.

---

## 3. Complexity Analysis

- **Time Complexity:** $O(N)$
  - Pass 1 traverses $N$ nodes to interweave clones $\implies O(N)$.
  - Pass 2 traverses $N$ original nodes to assign random pointers $\implies O(N)$.
  - Pass 3 separates the interleaved list of $2N$ nodes into two distinct lists $\implies O(N)$.
  - Total Time: $O(N) + O(N) + O(N) = O(N)$.
- **Space Complexity:** $O(1)$ Auxiliary Space
  - Only a few pointer variables (`curr`, `copy`, `copyHead`) are used. Zero auxiliary hash maps or dynamic arrays are allocated. (The $N$ new nodes belong to the required output list).

---

## 4. Edge Cases & Gotchas

- [x] **Empty List (`head == nullptr`):**
  - Handled immediately by `if (!head) return nullptr;`.
- [x] **Null Random Pointer (`curr->random == nullptr`):**
  - Must guard with `if (curr->random)` before evaluating `curr->random->next`. If null, `copy->random` remains `nullptr` as initialized.
- [x] **Self-Referential Random Pointer (`curr->random == curr`):**
  - Handled naturally: `curr->random->next` evaluates to `curr->next` (its own clone), correctly pointing `copy->random` to `copy`.
- [x] **Critical Deep Copy Invariant:**
  - Never write `copy->random = curr->random;`. That points the clone's random pointer to an **original** node, violating the strict deep copy requirement. It must be `copy->random = curr->random->next;`.
- [x] **Restoring Original List Integrity:**
  - Pass 3 must completely restore the original list's `next` links intact (`curr->next = copy->next;`). Leaving the original list mangled breaks caller invariants.

---

## 5. Clean Code (Optimal Solution: 3-Pass Interweaving)

```cpp
/*
// Definition for a Node.
class Node {
public:
    int val;
    Node* next;
    Node* random;

    Node(int _val) {
        val = _val;
        next = NULL;
        random = NULL;
    }
};
*/

class Solution {
public:
    Node* copyRandomList(Node* head) {
        if (!head) {
            return nullptr;
        }

        // 1. Insert copied node right after each original node.
        Node* curr = head;
        while (curr) {
            Node* copy = new Node(curr->val);
            copy->next = curr->next;
            curr->next = copy;
            curr = copy->next;
        }

        // 2. Set random pointers of copied nodes.
        curr = head;
        while (curr) {
            Node* copy = curr->next;
            if (curr->random) {
                copy->random = curr->random->next;
            }
            curr = copy->next;
        }

        // 3. Separate original list and copied list.
        Node* copyHead = head->next;
        curr = head;
        while (curr) {
            Node* copy = curr->next;
            curr->next = copy->next;
            if (copy->next) {
                copy->next = copy->next->next;
            }
            curr = curr->next;
        }

        return copyHead;
    }
};
```

---

## 6. Review & Takeaways

### Step-by-Step Dry Run

Given: `A -> B -> C` where:
- `A.random = C`
- `B.random = A`
- `C.random = nullptr`

#### Pass 1: Interweave Nodes
- Insert `a` after `A`, `b` after `B`, `c` after `C`:
  `A -> a -> B -> b -> C -> c -> nullptr`

#### Pass 2: Connect Random Pointers
- Node `A`: `A.random = C` $\implies$ `a.random = C.next = c`
- Node `B`: `B.random = A` $\implies$ `b.random = A.next = a`
- Node `C`: `C.random = nullptr` $\implies$ `c.random = nullptr`

#### Pass 3: Decouple Lists
- Unweave links:
  - Original: `A -> B -> C -> nullptr`
  - Cloned:   `a -> b -> c -> nullptr`
- With random pointers:
  - `a.random = c`
  - `b.random = a`
  - `c.random = nullptr`
- Return `copyHead` (`a`).

---

### The Architectural Pattern

```text
                  Copy List with Random Pointer
                                ↓
                 Pass 1: Interleave Clones In-Place
                    A  ──>  a  ──>  B  ──>  b  ──>  C  ──>  c
                                ↓
                 Pass 2: Set Cloned Random Pointers
                    copy->random = curr->random->next
                     (Uses original's next as map)
                                ↓
                 Pass 3: Decouple Both Linked Lists
                    Original:  A  ──>  B  ──>  C  ──>  nullptr
                    Copy:      a  ──>  b  ──>  c  ──>  nullptr
                                ↓
                         return copyHead
```

* **Next Review Date:** Low priority (benchmark interweaving pointer manipulation mastered).
* **Key Takeaway:** When mapping between original nodes and copied nodes with arbitrary cross-references, weave each clone immediately after its original node (`curr->next = copy`). The linked list structure itself serves as a temporary $O(1)$ auxiliary hash map (`original->random->next`).
