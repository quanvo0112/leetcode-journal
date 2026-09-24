# 0739. Daily Temperatures

- **Problem Link:** https://leetcode.com/problems/daily-temperatures/
- **Difficulty:** `Medium`
- **NeetCode Category:** `Stack`
- **LeetCode Topics:** `Array` / `Stack` / `Monotonic Stack`
- **Core Pattern:** `Monotonic Decreasing Stack (Store Indices, Resolve Next Greater Element)`
- **Last Practiced:** 2026-09-23
- **Proficiency Level:**
  - [x] Level 1: Solved smoothly (< 20 mins, optimal)
  - [ ] Level 2: Struggled / Non-optimal / Edge-case bugs
  - [ ] Level 3: Needed editorial or hints

---

## 1. Pattern Recognition & Triggers

- **Clues in prompt:**
  - *"Given an array of integers `temperatures` represents the daily temperatures"*
  - *"return an array `answer` such that `answer[i]` is the number of days you have to wait after the `i-th` day to get a warmer temperature."*
  - *"If there is no future day for which this is possible, keep `answer[i] == 0` instead."*
- **Core intuition:**
  - This is the classic **Next Greater Element** problem in disguise.
  - A brute-force scan from each index to the right takes $O(N^2)$, which TLEs for $N \le 10^5$.
  - Instead of actively searching to the right for every day, invert the thinking:
    $$\text{"Store unresolved days. When a warmer day arrives, resolve all waiting colder days that it surpasses."}$$
  - We maintain a **Monotonic Decreasing Stack** of indices where temperatures are in descending order from bottom to top:
    $$\text{temperatures}[\text{stack}[0]] \ge \text{temperatures}[\text{stack}[1]] \ge \text{temperatures}[\text{stack}[2]] \dots$$
  - When a warmer day `temperatures[i]` arrives, it resolves any colder days waiting at the top of the stack (`temperatures[i] > temperatures[prev]`).

---

## 2. Approach & Trade-offs

1. **Approach 1 — Brute-Force Nested Loops ($O(N^2)$ Time, $O(1)$ Extra Space):**
   - For each day $i$, scan $j$ from $i + 1$ to $N - 1$ until `temperatures[j] > temperatures[i]`.
   - *Verdict:* Inefficient $O(N^2)$. With $N = 10^5$, worst-case operations reach $10^{10}$, causing Time Limit Exceeded (TLE).

2. **Approach 2 — Monotonic Decreasing Stack (Optimal & Implemented):**
   - Use `vector<int> stack` to store indices of unresolved days.
   - For each current index `i`:
     - While stack is non-empty and `temperatures[i] > temperatures[stack.back()]`:
       - `prev = stack.back(); stack.pop_back();`
       - `result[prev] = i - prev;`
     - Push current index `i` into stack.
   - *Verdict:* Optimal $O(N)$ Time, $O(N)$ Space. Each index enters and leaves the stack at most once.

---

## 3. Complexity Analysis

- **Time Complexity:** $O(N)$
  - Although there is a nested `while` loop, every index from $0$ to $N - 1$ is pushed onto the stack **at most once** and popped **at most once**.
  - Across the entire execution, the inner loop runs at most $N$ times in total (amortized $O(1)$ per element).
- **Space Complexity:** $O(N)$
  - Output vector `result` of size $N$ takes $O(N)$ space.
  - In the worst case (strictly decreasing temperatures like `[80, 75, 70, 65]`), the stack holds all $N$ indices before the loop terminates ($O(N)$ auxiliary space).

---

## 4. Edge Cases & Gotchas

- [x] **Strictly Decreasing Temperatures (e.g. `[90, 80, 70]`):**
  - No future day is warmer. Elements remain in the stack until end. Because `result` is pre-initialized with `0`, all remain `0` correctly.
- [x] **Equal Temperatures (e.g. `[70, 70, 70]`):**
  - Condition is strictly greater: `temperatures[i] > temperatures[stack.back()]`.
  - Same temperatures do not resolve each other; they are pushed to stack and only resolved by a strictly warmer future day.
- [x] **Why store indices instead of temperatures?**
  - The problem requires the **number of waiting days** (`i - prev`).
  - If we only stored temperatures, we would lose spatial/temporal distance information. From index `prev`, the temperature is immediately retrieved via `temperatures[prev]`.

---

## 5. Clean Code (Optimal Solution: Monotonic Decreasing Stack)

```cpp
#include <vector>

using namespace std;

class Solution {
public:
    vector<int> dailyTemperatures(vector<int>& temperatures) {
        int n = temperatures.size();
        vector<int> result(n, 0);
        vector<int> stack; // Stores indices of unresolved colder days

        for (int i = 0; i < n; ++i) {
            // A warmer day has arrived: resolve all colder days waiting on the stack
            while (!stack.empty() && temperatures[i] > temperatures[stack.back()]) {
                int prev = stack.back();
                stack.pop_back();
                result[prev] = i - prev;
            }
            stack.push_back(i);
        }

        return result;
    }
};
```

---

## 6. Review & Takeaways

### Step-by-Step Dry Run

Given `temperatures = [73, 74, 75, 71, 69, 72, 76, 73]`:

```text
i=0 (temp=73): stack empty -> push 0.
               stack: [0]

i=1 (temp=74): 74 > temp[0] (73) -> resolve 0!
               result[0] = 1 - 0 = 1, pop 0 -> push 1.
               stack: [1]

i=2 (temp=75): 75 > temp[1] (74) -> resolve 1!
               result[1] = 2 - 1 = 1, pop 1 -> push 2.
               stack: [2]

i=3 (temp=71): 71 < temp[2] (75) -> cannot resolve.
               push 3.
               stack: [2, 3]

i=4 (temp=69): 69 < temp[3] (71) -> cannot resolve.
               push 4.
               stack: [2, 3, 4]

i=5 (temp=72):
  - 72 > temp[4] (69) -> resolve 4! result[4] = 5 - 4 = 1, pop 4.
  - 72 > temp[3] (71) -> resolve 3! result[3] = 5 - 3 = 2, pop 3.
  - 72 < temp[2] (75) -> stop while loop!
  - push 5.
  stack: [2, 5]

i=6 (temp=76):
  - 76 > temp[5] (72) -> resolve 5! result[5] = 6 - 5 = 1, pop 5.
  - 76 > temp[2] (75) -> resolve 2! result[2] = 6 - 2 = 4, pop 2.
  - push 6.
  stack: [6]

i=7 (temp=73): 73 < temp[6] (76) -> cannot resolve.
               push 7.
               stack: [6, 7]

End of loop: unresolved indices [6, 7] keep their default value 0.
Final result: [1, 1, 4, 2, 1, 1, 0, 0].
```

---

### The Architectural Pattern

```text
               Daily Temperatures
                       ↓
             Next Greater Element
                       ↓
           Monotonic Decreasing Stack
                 (Stores Indices)
                       ↓
  for i = 0 to n - 1:
    while !stack.empty() && temperatures[i] > temperatures[stack.back()]:
      prev = stack.pop()
      result[prev] = i - prev     <── Resolve waiting day
    stack.push(i)                 <── Add current day to waiting pool
```

* **Next Review Date:** Low priority (benchmark Next Greater Element monotonic stack pattern mastered).
* **Key Takeaway:** For any query asking for the **Next Greater / Warmer / Taller** element, maintain a **decreasing monotonic stack** of indices. New larger elements act as catalysts that pop and resolve pending smaller items.
