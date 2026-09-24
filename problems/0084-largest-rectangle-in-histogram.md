# 0084. Largest Rectangle in Histogram

- **Problem Link:** https://leetcode.com/problems/largest-rectangle-in-histogram/
- **Difficulty:** `Hard`
- **NeetCode Category:** `Stack`
- **LeetCode Topics:** `Array` / `Stack` / `Monotonic Stack`
- **Core Pattern:** `Monotonic Increasing Stack + Virtual Sentinel 0 (Previous & Next Smaller Element Boundaries)`
- **Last Practiced:** 2026-09-24
- **Proficiency Level:**
  - [x] Level 1: Solved smoothly (< 20 mins, optimal)
  - [ ] Level 2: Struggled / Non-optimal / Edge-case bugs
  - [ ] Level 3: Needed editorial or hints

---

## 1. Pattern Recognition & Triggers

- **Clues in prompt:**
  - *"Given an array of integers `heights` representing the histogram's bar height where the width of each bar is 1..."*
  - *"return the area of the largest rectangle in the histogram."*
  - $N \le 10^5$, $\text{heights}[i] \le 10^4$.
- **Core intuition:**
  - For any given bar $i$ with height $h = \text{heights}[i]$, what is the largest rectangle that uses $h$ as its limiting (minimum) height?
  - The rectangle can extend horizontally to the left until it hits the first bar strictly shorter than $h$ ($\text{leftSmaller}$ boundary).
  - Similarly, it can extend to the right until it hits the first bar strictly shorter than $h$ ($\text{rightSmaller}$ boundary).
  - The maximum width for a rectangle of height $h$ is:
    $$\text{width} = \text{rightSmaller} - \text{leftSmaller} - 1$$
    $$\text{area} = h \times \text{width}$$
  - Finding the **Previous Smaller Element** and **Next Smaller Element** for every bar independently takes $O(N^2)$ naively, but can be resolved in linear $O(N)$ time using a **Monotonic Increasing Stack**.

---

## 2. Approach & Trade-offs

1. **Approach 1 — Brute-Force All Pairs / Width Expansion ($O(N^2)$ Time, $O(1)$ Space):**
   - For every bar $i$, expand left and right to find where heights drop below $\text{heights}[i]$.
   - *Verdict:* $O(N^2)$ runtime will result in Time Limit Exceeded (TLE) for $N = 10^5$ ($10^{10}$ operations).

2. **Approach 2 — Precomputing `leftSmaller[]` & `rightSmaller[]` Arrays ($O(N)$ Time, $O(N)$ Extra Space):**
   - Use two separate passes with monotonic stacks to populate two boundary arrays `leftSmaller[N]` and `rightSmaller[N]`.
   - Then compute the area in a third pass: $\text{heights}[i] \times (\text{rightSmaller}[i] - \text{leftSmaller}[i] - 1)$.
   - *Verdict:* Valid $O(N)$, but requires 3 passes and $2N$ auxiliary array storage.

3. **Approach 3 — Single-Pass Monotonic Increasing Stack + Virtual Sentinel 0 (Chosen Optimal Solution):**
   - Maintain a `vector<int> stack` storing indices of bars in strictly non-decreasing height order:
     $$\text{heights}[\text{stack}[0]] \le \text{heights}[\text{stack}[1]] \le \text{heights}[\text{stack}[2]] \dots$$
   - When we encounter a bar at index $i$ with height strictly smaller than the bar at `stack.back()`:
     - The current index $i$ acts as the **right smaller boundary** for `stack.back()`.
     - Pop `mid = stack.back()` with height $h = \text{heights}[mid]$.
     - The new top of the stack is the **left smaller boundary**! If the stack becomes empty, it means there are no smaller bars to the left, so $\text{left} = -1$.
     - $\text{width} = i - \text{left} - 1$.
     - $\text{maxArea} = \max(\text{maxArea}, h \times \text{width})$.
   - **The Virtual Sentinel 0 Trick (`i <= heights.size()`):**
     - When the loop reaches index $N$, treat `currentHeight = 0`.
     - Because all bar heights are $\ge 0$, a height of `0` forces every remaining index in the stack to be popped and evaluated with $i = N$ as their right boundary.
   - *Verdict:* Optimal $O(N)$ Time, $O(N)$ Space. Single clean pass, zero auxiliary boundary arrays, zero manual end-of-loop stack draining code.

---

## 3. Complexity Analysis

- **Time Complexity:** $O(N)$
  - Each index from $0$ to $N - 1$ is pushed onto the stack exactly once and popped at most once.
  - The inner `while` loop runs at most $N$ times across the entire algorithm lifecycle (amortized $O(1)$ per bar).
- **Space Complexity:** $O(N)$
  - In the worst case (strictly increasing heights like `[1, 2, 3, 4, 5]`), the stack holds $N$ indices before being flushed by the sentinel $0$.
  - Auxiliary space is strictly $O(N)$.

---

## 4. Edge Cases & Gotchas

- [x] **Monotonically Increasing Heights (e.g. `[1, 2, 3, 4, 5]`):**
  - Without the sentinel $0$ at index $N$, bars would remain in the stack and never be evaluated.
  - The virtual sentinel `currentHeight = (i == n) ? 0 : heights[i]` guarantees 100% stack evacuation.
- [x] **All Bars of Equal Height (e.g. `[2, 2, 2, 2]`):**
  - Bars with equal heights are pushed or popped smoothly without incorrect boundaries; the widest rectangle covers all $N$ bars with $\text{height} \times N$.
- [x] **Single Bar ($N = 1$):**
  - Loop processes $i = 0$ (pushed), then $i = 1$ (sentinel 0 pops bar 0: $\text{left} = -1$, $\text{width} = 1 - (-1) - 1 = 1$, $\text{area} = \text{heights}[0] \times 1$). Returns correct area.
- [x] **Empty Stack after Pop (`left = -1`):**
  - When all elements to the left were taller and were already popped, the current bar extends all the way to index 0. Setting $\text{left} = -1$ gives $\text{width} = i - (-1) - 1 = i$, which correctly encompasses all indices from $0$ to $i - 1$.

---

## 5. Clean Code (Optimal Solution: Monotonic Increasing Stack + Sentinel 0)

```cpp
#include <vector>
#include <algorithm>

using namespace std;

class Solution {
public:
    int largestRectangleArea(vector<int>& heights) {
        vector<int> stack;
        int maxArea = 0;
        int n = heights.size();

        // Loop runs up to n (inclusive); index n acts as a virtual sentinel with height 0
        for (int i = 0; i <= n; ++i) {
            int currentHeight = (i == n) ? 0 : heights[i];

            // When a shorter bar is encountered, it bounds the right side of taller bars in the stack
            while (!stack.empty() && heights[stack.back()] > currentHeight) {
                int h = heights[stack.back()];
                stack.pop_back();

                // Left boundary is the new top of the stack (first smaller bar on the left)
                int left = stack.empty() ? -1 : stack.back();
                int width = i - left - 1;

                maxArea = max(maxArea, h * width);
            }

            if (i < n) {
                stack.push_back(i);
            }
        }

        return maxArea;
    }
};
```

---

## 6. Review & Takeaways

### Step-by-Step Dry Run

Given `heights = [2, 1, 5, 6, 2, 3]`:

```text
i=0 (h=2): stack empty -> push 0.
           stack: [0]

i=1 (h=1): currentHeight (1) < heights[0] (2) -> Pop 0!
           h = 2
           left = -1 (stack empty)
           width = 1 - (-1) - 1 = 1
           area = 2 * 1 = 2 -> maxArea = 2
           push 1.
           stack: [1]

i=2 (h=5): 5 > heights[1] (1) -> push 2.
           stack: [1, 2]

i=3 (h=6): 6 > heights[2] (5) -> push 3.
           stack: [1, 2, 3]

i=4 (h=2): currentHeight (2) < heights[3] (6) -> Pop 3!
           h = 6
           left = stack.back() = 2
           width = 4 - 2 - 1 = 1
           area = 6 * 1 = 6 -> maxArea = 6

           Still: currentHeight (2) < heights[2] (5) -> Pop 2!
           h = 5
           left = stack.back() = 1
           width = 4 - 1 - 1 = 2
           area = 5 * 2 = 10 -> maxArea = 10  <-- Optimal rectangle spanning indices [2, 3]

           currentHeight (2) > heights[1] (1) -> stop popping.
           push 4.
           stack: [1, 4]

i=5 (h=3): 3 > heights[4] (2) -> push 5.
           stack: [1, 4, 5]

i=6 (Virtual Sentinel h=0):
  - Pop 5 (h=3): left = 4, width = 6 - 4 - 1 = 1, area = 3 * 1 = 3
  - Pop 4 (h=2): left = 1, width = 6 - 1 - 1 = 4, area = 2 * 4 = 8
  - Pop 1 (h=1): left = -1, width = 6 - (-1) - 1 = 6, area = 1 * 6 = 6

Final maxArea = 10.
```

---

### The Architectural Pattern

```text
                  Largest Rectangle in Histogram
                                ↓
                 Previous & Next Smaller Elements
                                ↓
                    Monotonic Increasing Stack
                         (Stores Indices)
                                ↓
                Loop up to n (Sentinel 0 at index n)
                                ↓
            while !stack.empty() && heights[top] > currentHeight:
              ├─ h = heights[pop()]
              ├─ rightSmaller = i
              ├─ leftSmaller = stack.empty() ? -1 : stack.top()
              ├─ width = rightSmaller - leftSmaller - 1
              └─ maxArea = max(maxArea, h * width)
```

* **Next Review Date:** Low priority (benchmark geometric monotonic increasing stack pattern mastered).
* **Key Takeaway:** When searching for an optimal span bounded on both sides by smaller values, maintain a **strictly increasing stack**. The popping element provides height, the incoming index provides the right bound, the element below provides the left bound, and a virtual sentinel `0` guarantees complete resolution in a single pass.
