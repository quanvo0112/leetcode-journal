# 0287. Find the Duplicate Number

- **Problem Link:** https://leetcode.com/problems/find-the-duplicate-number/
- **Difficulty:** `Medium`
- **NeetCode Category:** `Linked List`
- **LeetCode Topics:** `Array` / `Two Pointers` / `Binary Search` / `Bit Manipulation`
- **Core Pattern:** `Floyd's Cycle Detection (Tortoise and Hare) on Virtual Linked List`
- **Last Practiced:** 2026-10-01
- **Proficiency Level:**
  - [x] Level 1: Solved smoothly (< 20 mins, optimal)
  - [ ] Level 2: Struggled / Non-optimal / Edge-case bugs
  - [ ] Level 3: Needed editorial or hints

---

## 1. Pattern Recognition & Triggers

- **Clues in prompt:**
  - Given an array of integers `nums` containing $n + 1$ integers where each integer is in the range $[1, n]$ inclusive.
  - There is only **one repeated number** in `nums`, return this duplicate.
  - Strict constraints: Must solve **without modifying the array** and using only **$O(1)$ constant extra space**.
- **Core intuition — The Virtual Linked List:**
  - A standard array index mapping $i \mapsto \text{nums}[i]$ defines a directed graph where each index $i$ has an outgoing edge to $\text{nums}[i]$.
  - Because $1 \le \text{nums}[i] \le n$ for all $0 \le i \le n$:
    1. No element equals $0$. Hence, index $0$ has an outgoing edge (`nums[0]`), but **no incoming edges**. Index $0$ acts as a guaranteed acyclic start node outside any cycle.
    2. By the **Pigeonhole Principle**, placing $n + 1$ items into $n$ slots guarantees at least one value $D$ occurs more than once.
    3. If two distinct indices $u$ and $v$ contain value $D$ ($\text{nums}[u] = \text{nums}[v] = D$), then both nodes $u$ and $v$ point to node $D$.
    4. A node with multiple incoming edges in a functional directed graph forms the **entrance of a cycle**.
  - Therefore, the problem is isomorphic to **Finding the Cycle Entrance in a Linked List** (LeetCode 142 / Floyd's Cycle-Finding Algorithm).

---

## 2. Approaches & Trade-offs

1. **Approach 1 — Hash Set ($O(N)$ time, $O(N)$ space):**
   - Store seen numbers in an `std::unordered_set<int>`.
   - *Drawback:* Violates the strict $O(1)$ auxiliary space constraint.

2. **Approach 2 — In-Place Array Mutation / Negation Marking ($O(N)$ time, $O(1)$ space):**
   - Traverse each value $x = |\text{nums}[i]|$, negate $\text{nums}[x]$. If $\text{nums}[x]$ is already negative, $x$ is the duplicate.
   - *Drawback:* Violates the explicit constraint: "You must solve the problem without modifying the array `nums`".

3. **Approach 3 — In-Place Sorting ($O(N \log N)$ time, $O(1)$ space):**
   - Sort the array and find adjacent identical elements (`nums[i] == nums[i+1]`).
   - *Drawback:* Violates the non-modification constraint and runs in sub-optimal $O(N \log N)$ time.

4. **Approach 4 — Binary Search on Range $[1, n]$ ($O(N \log N)$ time, $O(1)$ space):**
   - Binary search over the value range $[1, n]$. For $\text{mid}$, count elements in `nums` $\le \text{mid}$. If count $> \text{mid}$, duplicate lies in $[1, \text{mid}]$; otherwise in $[\text{mid} + 1, n]$.
   - *Drawback:* Valid non-destructive $O(1)$ space approach, but takes $O(N \log N)$ time due to repeated $O(N)$ counting passes.

5. **Approach 5 — Floyd's Cycle Detection / Tortoise and Hare (Chosen Optimal Solution):**
   - Interpret `nums[i]` as the `next` pointer of node $i$.
   - **Phase 1 (Detect Intersection):** Advance `slow = nums[slow]` (1 step) and `fast = nums[nums[fast]]` (2 steps) using a `do-while` loop until `slow == fast`. They are guaranteed to intersect inside the cycle.
   - **Phase 2 (Locate Cycle Entrance):** Reset `slow = nums[0]`, keeping `fast` at the meeting point. Advance both pointers **one step at a time** (`slow = nums[slow]; fast = nums[fast];`) until they meet. The collision point is the cycle entrance, which is the duplicate number.
   - *Verdict:* Optimal $O(N)$ time, strict $O(1)$ auxiliary space, and zero array modifications.

---

## 3. Complexity Analysis

- **Time Complexity:** $O(N)$
  - **Phase 1:** Let $L$ be the distance from index $0$ to the cycle entrance, and $C$ be the cycle length ($L + C \le N + 1$). The slow pointer takes $L$ steps to reach the cycle, and at most $C$ steps inside the cycle before being caught by `fast`. Total steps $\le L + C \le N + 1 \implies O(N)$.
  - **Phase 2:** Both pointers advance exactly $L$ steps to meet at the cycle entrance, where $L \le N$.
  - Total time is strictly linear $O(N)$.
- **Space Complexity:** $O(1)$ auxiliary space
  - Operates using only two integer pointer variables (`slow`, `fast`). Array is completely unmodified.

---

## 4. Edge Cases & Gotchas

- [x] **Smallest input size ($n = 1$, array size 2):** E.g., `nums = [1, 1]`. Phase 1 immediately meets at 1, Phase 2 confirms 1.
- [x] **Duplicate appears more than twice:** E.g., `nums = [2, 2, 2, 2, 2]`. Multiple branches converge to node 2, which still serves as the cycle entrance.
- [x] **Cycle contains all elements vs. tail before cycle:** Index 0 is never pointed to (values are in $[1, n]$), so there is always a non-empty prefix before the cycle entrance or index 0 directly points to the entrance.
- [x] **Do-While Loop vs. Initial While Loop:** Because both `slow` and `fast` start at `nums[0]`, an ordinary `while (slow != fast)` would exit immediately. A `do { ... } while (slow != fast);` guarantees at least one transition before checking collision.

---

## 5. Clean Code

```cpp
#include <vector>

using namespace std;

class Solution {
public:
    int findDuplicate(vector<int>& nums) {
        // Phase 1: Find intersection inside the cycle.
        int slow = nums[0];
        int fast = nums[0];

        do {
            slow = nums[slow];
            fast = nums[nums[fast]];
        } while (slow != fast);

        // Phase 2: Find the cycle entrance = duplicate number.
        slow = nums[0];

        while (slow != fast) {
            slow = nums[slow];
            fast = nums[fast];
        }

        return slow;
    }
};
```

---

## 6. Visual Walkthrough & Architectural Pattern

### Mathematical Proof of Phase 2

Let:
- $L$ = distance from index $0$ to the cycle entrance.
- $d$ = distance from the cycle entrance to the meeting point in Phase 1.
- $C$ = circumference of the cycle.

When `slow` and `fast` collide in Phase 1:
$$\text{Distance}(\text{slow}) = L + d$$
$$\text{Distance}(\text{fast}) = L + d + k \cdot C \quad (\text{for some integer } k \ge 1)$$

Since `fast` travels at twice the speed of `slow`:
$$2 \cdot \text{Distance}(\text{slow}) = \text{Distance}(\text{fast})$$
$$2(L + d) = L + d + k \cdot C$$
$$L + d = k \cdot C$$
$$L = k \cdot C - d = (k - 1)C + (C - d)$$

Notice that $(C - d)$ is the exact distance remaining from the meeting point to reach the cycle entrance again.
Therefore, if `slow` restarts from index $0$ and `fast` advances from the meeting point—both moving at **1 step per tick**:
- `slow` covers distance $L$ and arrives at the cycle entrance.
- `fast` covers distance $(k - 1)C + (C - d)$ and lands at the **exact same cycle entrance**.

```text
Index 0 ──(L steps)──> Entrance (Duplicate) ──(d steps)──> Meeting Point
                            ▲                                    │
                            └──────────(C - d steps)─────────────┘
```

---

### Step-by-Step Dry Run: `nums = [1, 3, 4, 2, 2]`

Directed Graph Mapping:
- $0 \to \text{nums}[0] = 1$
- $1 \to \text{nums}[1] = 3$
- $3 \to \text{nums}[3] = 2$
- $2 \to \text{nums}[2] = 4$
- $4 \to \text{nums}[4] = 2$

Graph Structure:
```text
0 ──> 1 ──> 3 ──> 2 ──> 4
                  ▲     │
                  └─────┘
```
Cycle entrance is **2** (the duplicate).

#### Phase 1: Meeting Point Detection
```text
Start: slow = nums[0] = 1, fast = nums[0] = 1

Tick 1:
  slow = nums[1] = 3
  fast = nums[nums[1]] = nums[3] = 2
  slow (3) != fast (2)

Tick 2:
  slow = nums[3] = 2
  fast = nums[nums[2]] = nums[4] = 2
  slow (2) == fast (2)  --> Collision confirmed at value 2!
```

#### Phase 2: Finding Cycle Entrance
```text
Reset slow = nums[0] = 1, keep fast = 2

Tick 1:
  slow = nums[1] = 3
  fast = nums[2] = 4
  slow (3) != fast (4)

Tick 2:
  slow = nums[3] = 2
  fast = nums[4] = 2
  slow (2) == fast (2)  --> Collision at Cycle Entrance = 2!

Return 2.
```

---

### The Architectural Pattern

```text
               Array with n + 1 elements in [1, n]
                                ↓
               Pigeonhole Principle: >= 1 Duplicate
                                ↓
               Define Virtual Edge: i -> nums[i]
                                ↓
        0 has no incoming edges (guaranteed start node)
        Duplicate has multiple incoming edges (cycle entrance)
                                ↓
        Phase 1: Floyd Fast / Slow (1 step vs 2 steps)
                                ↓
                        Meeting Point Inside Cycle
                                ↓
        Phase 2: Reset slow to nums[0], both move 1 step
                                ↓
                   Collision at Cycle Entrance
                                ↓
                         Duplicate Number
```

* **Next Review Date:** Low priority (virtual linked list cycle pattern mastered).
* **Key Takeaway:** When given an array of size $n+1$ containing values in $[1, n]$ with $O(1)$ space and read-only constraints, treat the array as a functional directed graph $i \to \text{nums}[i]$ and apply Floyd's Cycle Detection to locate the cycle entrance in $O(N)$ time.
