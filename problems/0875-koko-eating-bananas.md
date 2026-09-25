# 0875. Koko Eating Bananas

- **Problem Link:** https://leetcode.com/problems/koko-eating-bananas/
- **Difficulty:** `Medium`
- **NeetCode Category:** `Binary Search`
- **LeetCode Topics:** `Array` / `Binary Search`
- **Core Pattern:** `Binary Search on Answer (Lower Bound on Monotonic Feasibility Function)`
- **Last Practiced:** 2026-09-25
- **Proficiency Level:**
  - [x] Level 1: Solved smoothly (< 20 mins, optimal)
  - [ ] Level 2: Struggled / Non-optimal / Edge-case bugs
  - [ ] Level 3: Needed editorial or hints

---

## 1. Pattern Recognition & Triggers

- **Clues in prompt:**
  - *"Koko loves to eat bananas. There are `n` piles of bananas, the `i-th` pile has `piles[i]` bananas."*
  - *"The guards have gone and will come back in `h` hours."*
  - *"Koko can decide her bananas-per-hour eating speed of `k`... Return the minimum integer `k` such that she can eat all the bananas within `h` hours."*
  - Constraints: $N \le 10^4$, $\text{piles}[i] \le 10^9$, $h \le 10^9$, $N \le h$.
- **Core intuition:**
  - We are not searching for an element inside `piles`. Instead, we are searching for an **optimal value in the answer space**: the minimum eating speed $k$.
  - The valid speed range is bounded by $[1, \max(\text{piles})]$:
    - Minimum speed is $1$ (cannot eat 0 bananas/hr).
    - Maximum speed needed is $\max(\text{piles})$ because Koko can only eat from one pile per hour; increasing speed beyond $\max(\text{piles})$ will not reduce the total hours below $N$ (and $N \le h$ is guaranteed).
  - **Monotonicity of Feasibility Function:**
    - Let $f(k)$ be a boolean function: *"Can Koko finish all piles within $h$ hours at speed $k$?"*
    - If speed $k$ is sufficient to finish within $h$ hours, any higher speed $k' > k$ will also be sufficient.
    - Conversely, if speed $k$ is too slow, any lower speed will also be too slow.
    - This maps the solution space into a monotonic boolean sequence:
      $$\text{speeds: } [1, 2, 3, \dots, k-1, k, k+1, \dots]$$
      $$\text{feasible: } [\text{False}, \text{False}, \dots, \text{False}, \mathbf{\text{True}}, \text{True}, \dots]$$
    - Our goal is to find the **first `True`** (the minimum valid speed). This is the hallmark of **Binary Search on Answer**.

---

## 2. Approach & Trade-offs

1. **Approach 1 — Linear Scan on Speed ($O(N \cdot \max(\text{piles}))$ Time, $O(1)$ Space):**
   - Test speeds $k = 1, 2, 3, \dots$ sequentially until $f(k) == \text{true}$.
   - *Verdict:* Catastrophic TLE. With $\max(\text{piles}) \le 10^9$ and $N \le 10^4$, worst-case operations reach $10^{13}$, vastly exceeding the $10^8$ operations per second threshold.

2. **Approach 2 — Binary Search on Answer (Chosen Optimal Solution):**
   - Search space: `left = 1`, `right = *max_element(piles.begin(), piles.end())`.
   - While `left < right`:
     - Test candidate speed: `speed = left + (right - left) / 2`.
     - Calculate total hours required:
       $$\text{hours} = \sum_{i=0}^{N-1} \lceil \text{piles}[i] / \text{speed} \rceil$$
       In integer arithmetic: `(pile + speed - 1LL) / speed`.
     - If $\text{hours} \le h$: Speed is feasible, but a smaller speed might also work $\implies \text{right} = \text{speed}$.
     - If $\text{hours} > h$: Speed is too slow $\implies \text{left} = \text{speed} + 1$.
   - When `left == right`, the search space has converged to the minimal valid speed. Return `left`.
   - *Verdict:* Optimal $O(N \log(\max(\text{piles})))$ Time, strictly $O(1)$ Auxiliary Space.

---

## 3. Complexity Analysis

- **Time Complexity:** $O(N \log(\max(\text{piles})))$
  - Finding $\max(\text{piles})$ takes $O(N)$ time.
  - The binary search range $[1, 10^9]$ requires at most $\lceil \log_2(10^9) \rceil \approx 30$ iterations.
  - In each iteration, evaluating feasibility scans all $N$ piles in $O(N)$ time (with an early `break` optimization if `hours > h`).
  - Total operations: $30 \times 10^4 \approx 3 \times 10^5$, well under 10 milliseconds.
- **Space Complexity:** $O(1)$
  - No auxiliary data structures allocated; only scalar variables (`left`, `right`, `speed`, `hours`) are maintained on the stack.

---

## 4. Edge Cases & Gotchas

- [x] **64-bit Integer Overflow in Hour Accumulation:**
  - If speed is small (e.g. $k = 1$) and piles are large ($10^4$ piles of $10^9$ bananas), the total hours sum can reach $10^4 \times 10^9 = 10^{13}$.
  - $10^{13}$ exceeds the 32-bit signed integer limit ($2 \times 10^9$). Using `long long hours = 0;` is mandatory.
- [x] **Integer Overflow in Ceiling Formula:**
  - Computing `(pile + speed - 1)` can overflow if `pile` is $10^9$ and `speed` is $10^9$ ($10^9 + 10^9 - 1 \approx 2 \times 10^9$, close to `INT_MAX`).
  - Using `1LL` as in `(pile + speed - 1LL) / speed` promotes the addition to 64-bit `long long`, avoiding overflow completely.
- [x] **Why `right = speed` instead of `right = speed - 1`?**
  - If candidate `speed` is valid (`hours <= h`), it could itself be the minimal valid answer. Discarding it with `speed - 1` could eliminate the correct solution. Keeping `right = speed` preserves the invariant that the answer is always contained within $[left, right]$.
- [x] **Early Termination Optimization:**
  - Inside the pile iteration: `if (hours > h) break;` halts the loop immediately once the time limit is exceeded, pruning unnecessary arithmetic.

---

## 5. Clean Code (Optimal Solution: Binary Search on Answer)

```cpp
#include <vector>
#include <algorithm>

using namespace std;

class Solution {
public:
    int minEatingSpeed(vector<int>& piles, int h) {
        int left = 1;
        int right = *max_element(piles.begin(), piles.end());

        // Invariant: the minimum valid speed is always within [left, right]
        while (left < right) {
            int speed = left + (right - left) / 2;
            long long hours = 0;

            for (int pile : piles) {
                // Integer ceil: ceil(pile / speed) == (pile + speed - 1LL) / speed
                hours += (pile + speed - 1LL) / speed;
                if (hours > h) {
                    break; // Early prune: this speed already exceeds the allowed time
                }
            }

            if (hours <= h) {
                // Current speed is feasible; search left to find if a smaller speed works
                right = speed;
            } else {
                // Current speed is too slow; answer must be strictly larger
                left = speed + 1;
            }
        }

        return left; // Converged where left == right
    }
};
```

---

## 6. Review & Takeaways

### Step-by-Step Dry Run

Given `piles = [3, 6, 7, 11]`, `h = 8`:

```text
Initial range: left = 1, right = max(piles) = 11

Iteration 1:
  speed = 1 + (11 - 1) / 2 = 6
  Hours calculation:
    pile 3:  (3 + 5) / 6 = 1 hr
    pile 6:  (6 + 5) / 6 = 1 hr
    pile 7:  (7 + 5) / 6 = 2 hrs
    pile 11: (11 + 5) / 6 = 2 hrs
    total hours = 1 + 1 + 2 + 2 = 6 hrs
  6 <= 8 (Feasible!) -> right = 6
  Active range: [1, 6]

Iteration 2:
  speed = 1 + (6 - 1) / 2 = 3
  Hours calculation:
    pile 3:  (3 + 2) / 3 = 1 hr
    pile 6:  (6 + 2) / 3 = 2 hrs
    pile 7:  (7 + 2) / 3 = 3 hrs
    pile 11: (11 + 2) / 3 = 4 hrs
    total hours = 1 + 2 + 3 + 4 = 10 hrs
  10 > 8 (Too slow!) -> left = 3 + 1 = 4
  Active range: [4, 6]

Iteration 3:
  speed = 4 + (6 - 4) / 2 = 5
  Hours calculation:
    pile 3:  (3 + 4) / 5 = 1 hr
    pile 6:  (6 + 4) / 5 = 2 hrs
    pile 7:  (7 + 4) / 5 = 2 hrs
    pile 11: (11 + 4) / 5 = 3 hrs
    total hours = 1 + 2 + 2 + 3 = 8 hrs
  8 <= 8 (Feasible!) -> right = 5
  Active range: [4, 5]

Iteration 4:
  speed = 4 + (5 - 4) / 2 = 4
  Hours calculation:
    pile 3:  (3 + 3) / 4 = 1 hr
    pile 6:  (6 + 3) / 4 = 2 hrs
    pile 7:  (7 + 3) / 4 = 2 hrs
    pile 11: (11 + 3) / 4 = 3 hrs
    total hours = 1 + 2 + 2 + 3 = 8 hrs
  8 <= 8 (Feasible!) -> right = 4
  Active range: [4, 4]

Loop terminates (left == right == 4).
Result: 4.
```

---

### The Architectural Pattern

```text
               Binary Search on Answer Pattern
                            ↓
               Search Range: [1, max(piles)]
                            ↓
                   while left < right:
                            ↓
                 mid = left + (right - left) / 2
                            ↓
                 feasibilityCheck(mid) ?
                 (hours(mid) <= h ?)
                   /              \
             YES  /                \  NO
                 ↓                  ↓
          right = mid         left = mid + 1
       (Preserve valid       (Discard invalid
          candidate)             half)
                 \                  /
                  \                /
                   └───────┬──────┘
                           ↓
                   left == right (First True)
```

* **Next Review Date:** Low priority (benchmark Binary Search on Answer pattern mastered).
* **Key Takeaway:** Whenever asked to find the **minimum or maximum value satisfying a monotonic threshold condition**, apply Binary Search on the answer space. Use `while (left < right)` with `right = mid` and `left = mid + 1` to converge directly onto the first valid boundary.
