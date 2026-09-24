# 0239. Sliding Window Maximum

- **Problem Link:** https://leetcode.com/problems/sliding-window-maximum/
- **Difficulty:** `Hard`
- **NeetCode Category:** `Sliding Window`
- **LeetCode Topics:** `Array` / `Queue` / `Sliding Window` / `Heap (Priority Queue)` / `Monotonic Queue` / `Range Minimum/Maximum Query`
- **Core Pattern:** `Monotonic Decreasing Deque (Store Indices, Front is Max)`
- **Last Practiced:** 2026-09-22
- **Proficiency Level:**
  - [x] Level 1: Solved smoothly (< 20 mins, optimal)
  - [ ] Level 2: Struggled / Non-optimal / Edge-case bugs
  - [ ] Level 3: Needed editorial or hints

---

## 1. Pattern Recognition & Triggers

- **Clues in prompt:** *"You are given an array of integers `nums`, there is a sliding window of size `k` which is moving from the very left of the array to the very right"*, *"You can only see the `k` numbers in the window"*, *"Return the max sliding window"*, $N \le 10^5$, $k \le N$.
- **Core intuition:**
  - We do not need to preserve every single element inside the sliding window.
  - We only need to preserve **viable candidates** that have any possibility of becoming the maximum in the current or upcoming windows.
  - If we have an older element in the window with value $A$, and a newly arrived element with value $B \ge A$:
    - $B$ is **larger** than $A$.
    - $B$ is **younger** (will remain in the window longer into the future than $A$).
    - Therefore, $A$ can **never** become the maximum again for any window containing $B$. $A$ can be permanently discarded!
  - This property guarantees that viable candidates form a **Monotonic Decreasing Sequence** from front to back:
    $$nums[dq[0]] \ge nums[dq[1]] \ge nums[dq[2]] \ge \dots$$
  - Consequently, the front of the deque $nums[dq.front()]$ **always holds the maximum** of the current active window in $O(1)$!

---

## 2. Approach & Trade-offs

1. **Approach 1 — Brute Force Scan ($O(N \cdot K)$ Time, $O(1)$ Extra Space):**
   - For every of the $(N - K + 1)$ windows, scan all $K$ elements to determine the maximum.
   - *Verdict:* With $N = 10^5, K = 5 \times 10^4$, operations reach $5 \times 10^9 \rightarrow$ Time Limit Exceeded (TLE).

2. **Approach 2 — Max Heap / Priority Queue ($O(N \log N)$ or $O(N \log K)$ Time, $O(N)$ Space):**
   - Maintain a `priority_queue<pair<int, int>>` storing `{value, index}`.
   - At each step, push the new element, pop top elements whose index $\le right - K$, and read `pq.top().first`.
   - *Verdict:* Valid, but adds $O(\log N)$ or $O(\log K)$ overhead per element. Suboptimal compared to linear time.

3. **Approach 3 — Monotonic Decreasing Deque (Optimal & Implemented):**
   - Store **indices** (not values) in a `std::deque<int>` to easily check for window expiration.
   - At each step $right$:
     1. **Evict expired indices from front:** `while (!dq.empty() && dq.front() <= right - k) dq.pop_front();`
     2. **Evict smaller values from back:** `while (!dq.empty() && nums[dq.back()] <= nums[right]) dq.pop_back();`
     3. **Enqueue current index:** `dq.push_back(right);`
     4. **Record maximum:** When $right \ge k - 1$, append $nums[dq.front()]$ to result.
   - *Verdict:* Optimal $O(N)$ time, $O(K)$ space. Amortized $O(1)$ operations per element.

---

## 3. Complexity Analysis

- **Time Complexity:** $O(N)$
  - Despite the nested `while` loops, each index from $0$ to $N - 1$:
    - Is pushed into the back of the deque **at most once**.
    - Is popped from the back **at most once** (when superseded by a larger number).
    - Is popped from the front **at most once** (when expired from the window).
  - Total number of deque operations across the entire algorithm is bounded by $3N \rightarrow O(N)$.
- **Space Complexity:** $O(K)$
  - The deque only holds indices belonging to the current window of size $K$. At any instant, $|dq| \le K$.

---

## 4. Edge Cases & Gotchas

- [x] **Store Indices, NOT Values:**
  - The deque must store **indices** rather than raw values because we need to determine whether the front element has expired outside the window boundary (`dq.front() <= right - k`).
- [x] **Why `<=` instead of `<` when popping the back?**
  ```cpp
  while (!dq.empty() && nums[dq.back()] <= nums[right]) {
      dq.pop_back();
  }
  ```
  - Consider $nums = [1, 3, 3]$ with $k = 2$:
  - When reaching the second $3$, the first $3$ will expire before the second $3$. Since the second $3$ has an identical value and a strictly longer lifespan, the earlier $3$ is completely redundant.
  - Using `<=` keeps the deque strictly leaner and eliminates duplicates.
- [x] **$K = 1$:** The window size is 1; every element is its own maximum. The output is identical to `nums`.
- [x] **$K = N$:** Single window spanning the entire array; returns a single maximum value.
- [x] **Strictly decreasing array (e.g. `[5, 4, 3, 2, 1]`):** No elements are popped from the back; all indices enter the deque and pop strictly from the front upon expiration.
- [x] **Strictly increasing array (e.g. `[1, 2, 3, 4, 5]`):** Every new element clears all previous elements from the back; deque maintains size 1.

---

## 5. Clean Code (Optimal Solution: Monotonic Deque)

```cpp
#include <vector>
#include <deque>

using namespace std;

class Solution {
public:
    vector<int> maxSlidingWindow(vector<int>& nums, int k) {
        deque<int> dq; // Monotonic decreasing deque storing indices
        vector<int> result;
        result.reserve(nums.size() - k + 1);

        for (int right = 0; right < nums.size(); ++right) {
            // 1. Evict indices that fall outside the active window boundary
            while (!dq.empty() && dq.front() <= right - k) {
                dq.pop_front();
            }

            // 2. Maintain monotonic decreasing order:
            // Discard elements smaller than or equal to nums[right] from the back,
            // as they can never become the maximum in any window containing nums[right]
            while (!dq.empty() && nums[dq.back()] <= nums[right]) {
                dq.pop_back();
            }

            // 3. Enqueue the current element's index
            dq.push_back(right);

            // 4. Once the window reaches full size k, record the maximum at the front
            if (right >= k - 1) {
                result.push_back(nums[dq.front()]);
            }
        }

        return result;
    }
};
```

---

## 6. Review & Takeaways

### Step-by-Step Dry Run

Given `nums = [1, 3, -1, -3, 5, 3, 6, 7]`, `k = 3`:

```text
right = 0 (val = 1):
  pop_front: none
  pop_back: none
  push 0 -> dq: [0(1)]
  right < 2 -> no output

right = 1 (val = 3):
  pop_front: none
  pop_back: 1 <= 3 -> pop index 0
  push 1 -> dq: [1(3)]
  right < 2 -> no output

right = 2 (val = -1):
  pop_front: none
  pop_back: none (-1 < 3)
  push 2 -> dq: [1(3), 2(-1)]
  right >= 2 -> result.push_back(nums[1]) = 3
  Window [1, 3, -1] -> Max = 3

right = 3 (val = -3):
  pop_front: none (1 > 3 - 3)
  pop_back: none (-3 < -1)
  push 3 -> dq: [1(3), 2(-1), 3(-3)]
  right >= 2 -> result.push_back(nums[1]) = 3
  Window [3, -1, -3] -> Max = 3

right = 4 (val = 5):
  pop_front: dq.front()=1 <= 4 - 3=1 -> pop index 1!
  pop_back: nums[3]=-3 <= 5 -> pop index 3
            nums[2]=-1 <= 5 -> pop index 2
  push 4 -> dq: [4(5)]
  right >= 2 -> result.push_back(nums[4]) = 5
  Window [-1, -3, 5] -> Max = 5

right = 5 (val = 3):
  pop_front: none
  pop_back: none (3 < 5)
  push 5 -> dq: [4(5), 5(3)]
  right >= 2 -> result.push_back(nums[4]) = 5
  Window [-3, 5, 3] -> Max = 5

right = 6 (val = 6):
  pop_front: none
  pop_back: 3 <= 6 -> pop 5; 5 <= 6 -> pop 4
  push 6 -> dq: [6(6)]
  right >= 2 -> result.push_back(nums[6]) = 6
  Window [5, 3, 6] -> Max = 6

right = 7 (val = 7):
  pop_front: none
  pop_back: 6 <= 7 -> pop 6
  push 7 -> dq: [7(7)]
  right >= 2 -> result.push_back(nums[7]) = 7
  Window [3, 6, 7] -> Max = 7

Final Output: [3, 3, 5, 5, 6, 7]
```

---

### The 3 Core Operations of Monotonic Deque

```text
                  [ Front ]  ──────────────>  [ Back ]
             (Maximum Value)             (Smallest Value)
                    ▲                           │
                    │                           ▼
             pop_front() if expired       pop_back() while <= incoming
             (index <= right - k)         then push_back(incoming)
```

---

### The Architectural Pattern

```text
Sliding Window Maximum
          ↓
   Monotonic Deque (indices)
          ↓
  for right in 0 .. n - 1:
          ├─ 1. while dq.front() <= right - k:
          │          dq.pop_front()              (remove expired)
          ├─ 2. while nums[dq.back()] <= nums[right]:
          │          dq.pop_back()               (maintain decreasing)
          ├─ 3. dq.push_back(right)
          └─ 4. if right >= k - 1:
                     result.push_back(nums[dq.front()])
          ↓
    return result
```

* **Next Review Date:** Low priority (benchmark monotonic deque pattern mastered).
* **Key Takeaway:** For any fixed or sliding window min/max query, a **monotonic deque** provides optimal $O(N)$ performance by storing indices in decreasing (or increasing) order and discarding candidates that are both older and smaller than newly arriving elements.

