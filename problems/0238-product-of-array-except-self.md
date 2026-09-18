# 0238. Product of Array Except Self

- **Problem Link:** https://leetcode.com/problems/product-of-array-except-self/
- **Difficulty:** `Medium`
- **Topic / Pattern:** `Array` / `Prefix Sum (Product)`
- **Last Practiced:** 2026-09-18
- **Proficiency Level:** 
  - [x] 🟢 Level 1: Solved smoothly (< 20 mins, optimal)
  - [ ] 🟡 Level 2: Struggled / Non-optimal / Edge-case bugs
  - [ ] 🔴 Level 3: Needed editorial or hints

---

## 1. Pattern Recognition & Triggers
- Clues in prompt: *"product of all the elements of nums except nums[i]"*, *"without using the division operator"*, *"O(n) time"*, *"O(1) extra space complexity"*.
- Core intuition: For any index $i$, the answer is mathematically split into two independent parts:
  $$\text{result}[i] = (\text{product of elements to the left of } i) \times (\text{product of elements to the right of } i)$$
  Instead of allocating auxiliary arrays for both sides, compute the prefix products directly inside `result`, then multiply by suffix products on a reverse pass using a single running accumulator variable.

---

## 2. Approach & Trade-offs

1. **Approach 1 — Total Product with Division (Forbidden & Fragile):**
   - Calculate total product of the array, then for each element compute `total / nums[i]`.
   - *Failure:* Strictly prohibited by problem constraints. Furthermore, it crashes or requires ugly branching if array contains zeros (one zero vs multiple zeros).

2. **Approach 2 — Explicit Prefix and Suffix Arrays ($O(N)$ Space):**
   - Allocate two separate arrays: `prefix[n]` and `suffix[n]`.
   - Compute `result[i] = prefix[i - 1] * suffix[i + 1]`.
   - *Trade-off:* Clear and easy to reason about, but consumes $2N$ auxiliary space.

3. **Approach 3 — Two-Pass In-Place Accumulator (Optimal & Implemented):**
   - **Pass 1 (Left $\rightarrow$ Right):** Store prefix products directly in `result[i]` while updating running `prefix`.
   - **Pass 2 (Right $\rightarrow$ Left):** Multiply `result[i]` by running `suffix` while updating `suffix`.
   - *Verdict:* $O(N)$ time and strictly $O(1)$ auxiliary space (excluding the output array).

---

## 3. Complexity Analysis
Let $N = \text{nums.size()}$.

- **Time Complexity:** $O(N)$
  - Forward prefix pass: $N$ iterations.
  - Backward suffix pass: $N$ iterations.
  - Total: $2N \implies O(N)$ linear time.
- **Space Complexity:** $O(1)$ extra space
  - Uses only two scalar variables: `prefix` and `suffix`.
  - The returned vector `result` of size $N$ is required by the problem and does not count towards auxiliary space.

---

## 4. Edge Cases & Gotchas
- [x] **Array with a single zero (e.g. `[1, 2, 0, 4]`):** Produces `[0, 0, 8, 0]` naturally without any special-case branching. The zero causes `prefix` to become 0 for elements to its right, and `suffix` to become 0 for elements to its left.
- [x] **Array with multiple zeros (e.g. `[0, 1, 0]`):** Evaluates correctly to `[0, 0, 0]`.
- [x] **Negative numbers:** Handled transparently by standard integer multiplication rules.
- [x] **Smallest input size ($N = 2$):** Correctly computes `[nums[1], nums[0]]`.

---

## 5. Clean Code (Prefix + Suffix In-Place)

```cpp
class Solution {
public:
    vector<int> productExceptSelf(vector<int>& nums) {
        int n = nums.size();
        vector<int> result(n, 1);

        // Pass 1: result[i] stores product of all elements to the left of i
        int prefix = 1;
        for (int i = 0; i < n; ++i) {
            result[i] = prefix;
            prefix *= nums[i];
        }

        // Pass 2: Multiply by product of all elements to the right of i
        int suffix = 1;
        for (int i = n - 1; i >= 0; --i) {
            result[i] *= suffix;
            suffix *= nums[i];
        }

        return result;
    }
};
```

---

## 6. Review & Takeaways

### 🔍 Dry Run Walkthrough

```text
nums = [1, 2, 3, 4]

1. Pass 1: Prefix Accumulation (Left to Right)
   i = 0: result[0] = 1,      prefix = 1 * 1 = 1
   i = 1: result[1] = 1,      prefix = 1 * 2 = 2
   i = 2: result[2] = 2,      prefix = 2 * 3 = 6
   i = 3: result[3] = 6,      prefix = 6 * 4 = 24
   After Pass 1: result = [1, 1, 2, 6]

2. Pass 2: Suffix Multiplication (Right to Left)
   suffix = 1
   i = 3: result[3] = 6 * 1 = 6,    suffix = 1 * 4 = 4
   i = 2: result[2] = 2 * 4 = 8,    suffix = 4 * 3 = 12
   i = 1: result[1] = 1 * 12 = 12,  suffix = 12 * 2 = 24
   i = 0: result[0] = 1 * 24 = 24,  suffix = 24 * 1 = 24
   After Pass 2: result = [24, 12, 8, 6]
```

---

### 💡 Visualizing the Accumulation Pattern

```text
                 Prefix Pass (→)
nums   = [  1,       2,       3,       4  ]
result = [  1,       1,       2,       6  ]

                 Suffix Pass (←)
suffix = [ 24,      12,       4,       1  ]
-------------------------------------------
result = [ 24,      12,       8,       6  ]
```

Instead of allocating memory for both `prefix[]` and `suffix[]`, we reuse the output buffer `result` for the prefix pass, and stream the suffix pass using a single scalar variable `suffix`.

---

### 💬 Interview Pitch: *"Why this solution?"*

> *"I use two linear passes. The first pass traverses from left to right, storing the cumulative product of all elements to the left of each index directly inside the result array. The second pass traverses from right to left, multiplying each entry by a running suffix product of all elements to its right. This achieves $O(N)$ time complexity while maintaining strictly $O(1)$ auxiliary space."*

* **Next Review Date:** Low priority (benchmark prefix-product pattern).
* **Key Takeaway:** When calculating symmetric left/right aggregates without extra space, populate the output array in the forward direction, then fold the reverse aggregate in-place using a scalar accumulator.
