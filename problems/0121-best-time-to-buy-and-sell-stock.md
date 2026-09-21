# 0121. Best Time to Buy and Sell Stock

- **Problem Link:** https://leetcode.com/problems/best-time-to-buy-and-sell-stock/
- **Difficulty:** `Easy`
- **NeetCode Category:** `Sliding Window`
- **LeetCode Topics:** `Array` / `Dynamic Programming`
- **Core Pattern:** `Greedy + Running Minimum (minPrice Tracking)`
- **Last Practiced:** 2026-09-20
- **Proficiency Level:** 
  - [x] Level 1: Solved smoothly (< 20 mins, optimal)
  - [ ] Level 2: Struggled / Non-optimal / Edge-case bugs
  - [ ] Level 3: Needed editorial or hints

---

## 1. Pattern Recognition & Triggers

- **Clues in prompt:** *"choose a single day to buy one stock and choose a different day in the future to sell that stock"*, *"maximize your profit"*, *"return 0 if you cannot achieve any profit"*.
- **Core intuition:**
  - We want to maximize:
    $$\text{Profit} = prices[sell] - prices[buy] \quad \text{where} \quad buy < sell$$
  - At any arbitrary selling day $i$, the maximum possible profit is achieved if we had bought on the day with the **lowest price strictly before day $i$**.
  - We do not need to look forward into the future or keep a full history of all past prices. Maintaining a single running scalar variable `minPrice` as we scan left-to-right provides all the information needed to evaluate the optimal profit on day $i$:
    $$\text{potential\_profit}[i] = prices[i] - minPrice$$

---

## 2. Approach & Trade-offs

1. **Approach 1 — Brute Force ($O(N^2)$ Time, $O(1)$ Space):**
   - Use two nested loops to evaluate every valid pair $(i, j)$ with $i < j$.
   - *Verdict:* With $N = 10^5$, $N^2 = 10^{10}$ operations $\rightarrow$ Time Limit Exceeded (TLE).

2. **Approach 2 — Sliding Window ($O(N)$ Time, $O(1)$ Space):**
   - Maintain `left` (buy day) and `right` (sell day). If $prices[right] > prices[left]$, compute profit and advance `right`. If $prices[right] < prices[left]$, reset `left = right`.
   - *Verdict:* Valid and optimal, but conceptually equivalent to tracking a running minimum while requiring more index management.

3. **Approach 3 — Greedy with Running Minimum (Optimal & Implemented):**
   - Initialize `minPrice = prices[0]` and `maxProfit = 0`.
   - Iterate $i$ from $1$ to $n - 1$:
     - Compute potential profit: `maxProfit = max(maxProfit, prices[i] - minPrice);`
     - Update running floor: `minPrice = min(minPrice, prices[i]);`
   - *Verdict:* Cleanest and most direct $O(N)$ time, $O(1)$ space solution. Zero allocation, cache-friendly, single pass.

---

## 3. Complexity Analysis

- **Time Complexity:** $O(N)$
  - A single linear scan through the array of length $N$. Each price is examined exactly once.
- **Space Complexity:** $O(1)$
  - Only two scalar integers (`minPrice`, `maxProfit`) allocated on the stack.

---

## 4. Edge Cases & Gotchas

- [x] **Order of updates (Crucial Gotcha):**
  ```cpp
  maxProfit = max(maxProfit, prices[i] - minPrice);
  minPrice = min(minPrice, prices[i]);
  ```
  Updating `maxProfit` *before* `minPrice` ensures that `minPrice` strictly represents the lowest price seen on days **prior** to day $i$. Buying and selling on the exact same day in a single transaction is conceptually avoided.
- [x] **Strictly descending prices (e.g. `prices = [7, 6, 4, 3, 1]`):** No profitable transactions exist. `prices[i] - minPrice` is always negative or zero. Returns `0`.
- [x] **Flat prices (e.g. `prices = [5, 5, 5, 5]`):** Difference is always `0`. Returns `0`.
- [x] **Minimum input size ($N = 1$):** Loop from $i = 1$ to $0$ does not execute; immediately returns `maxProfit = 0`.

---

## 5. Clean Code (Optimal Solution: Greedy + Running Minimum)

```cpp
class Solution {
public:
    int maxProfit(vector<int>& prices) {
        int minPrice = prices[0];
        int maxProfit = 0;

        for (int i = 1; i < prices.size(); ++i) {
            // Evaluate profit if selling today using the minimum purchase price seen so far
            maxProfit = max(maxProfit, prices[i] - minPrice);

            // Update the minimum purchase price for future selling opportunities
            minPrice = min(minPrice, prices[i]);
        }

        return maxProfit;
    }
};
```

---

## 6. Review & Takeaways

### Step-by-Step Dry Run

Given `prices = [7, 1, 5, 3, 6, 4]`:

```text
Initial state: minPrice = 7, maxProfit = 0

i = 1 (price = 1):
  profit = 1 - 7 = -6 -> maxProfit = max(0, -6) = 0
  minPrice = min(7, 1) = 1

i = 2 (price = 5):
  profit = 5 - 1 = 4  -> maxProfit = max(0, 4) = 4
  minPrice = min(1, 5) = 1

i = 3 (price = 3):
  profit = 3 - 1 = 2  -> maxProfit = max(4, 2) = 4
  minPrice = min(1, 3) = 1

i = 4 (price = 6):
  profit = 6 - 1 = 5  -> maxProfit = max(4, 5) = 5
  minPrice = min(1, 6) = 1

i = 5 (price = 4):
  profit = 4 - 1 = 3  -> maxProfit = max(5, 3) = 5
  minPrice = min(1, 4) = 1

Result: 5 (Buy at price 1 on day 1, Sell at price 6 on day 4).
```

---

### Why Not Bidirectional Two Pointers?

While classified under Sliding Window in NeetCode 150, this problem does **not** employ converging two pointers (`left → ... ← right`). 

Instead, it embodies **Single Pass + Running Minimum**:
- At each step $i$, we make a locally optimal greedy inquiry: *"If I were forced to sell today, what was the cheapest purchase price available before today?"*
- By persisting `minPrice`, we collapse the entire prefix history into an $O(1)$ scalar query.

---

### The Architectural Pattern

```text
Best Time to Buy and Sell Stock
              ↓
     Single Pass / Greedy
              ↓
  track running minPrice (prices[0])
              ↓
  for each day i from 1 to n - 1:
    ├─ maxProfit = max(maxProfit, prices[i] - minPrice)
    └─ minPrice  = min(minPrice, prices[i])
              ↓
       return maxProfit
```

* **Next Review Date:** Low priority (benchmark prefix-minimum greedy pattern mastered).
* **Key Takeaway:** When maximizing the difference $A[j] - A[i]$ with chronological constraint $i < j$, compress the past history into a single running minimum accumulator during a forward linear scan.
