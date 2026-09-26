# 0347. Top K Frequent Elements

- **Problem Link:** https://leetcode.com/problems/top-k-frequent-elements/
- **Difficulty:** `Medium`
- **NeetCode Category:** `Arrays & Hashing`
- **LeetCode Topics:** `Array` / `Hash Table` / `Divide and Conquer` / `Sorting` / `Heap (Priority Queue)` / `Bucket Sort` / `Counting` / `Quickselect`
- **Core Pattern:** `Bucket Sort (Count as Index) in O(N) Time`
- **Last Practiced:** 2026-09-18
- **Proficiency Level:**
  - [x] Level 1: Solved smoothly (< 20 mins, optimal)
  - [ ] Level 2: Struggled / Non-optimal / Edge-case bugs
  - [ ] Level 3: Needed editorial or hints

---

## 1. Pattern Recognition & Triggers
- Clues in prompt: *"return the k most frequent elements"*, *"algorithm's time complexity must be better than O(n log n)"*, *$-10^4 \le \text{nums}[i] \le 10^4$*.
- Core intuition: We need to group numbers by their appearance counts and retrieve the highest frequencies. Since an element's frequency is strictly bounded by $[1, N]$, we can invert the relationship (`frequency -> list of numbers`) using **Bucket Sort** in $O(N)$ time. Furthermore, because value magnitudes are bounded within $[-10000, 10000]$ ($V = 20,001$ unique values), a direct **Frequency Array** avoids `unordered_map` hashing overhead and collisions entirely.

---

## 2. Approach & Trade-offs

1. **Sorting ($O(N \log N)$):**
   - Count frequencies, sort elements based on frequency in descending order.
   - *Verdict:* Fails LeetCode's follow-up constraint requiring better than $O(N \log N)$.

2. **Min-Heap / `priority_queue` ($O(N \log K)$):**
   - Count frequencies with a hash map, push into a min-heap of size $K$. If heap size exceeds $K$, pop the minimum.
   - *Verdict:* Valid and optimal when $K \ll N$ or in streaming scenarios, but incurs $O(\log K)$ heap rebalancing overhead per element.

3. **Frequency Array + Bucket Sort (Optimal & Implemented):**
   - **Step 1:** Count frequencies using a fixed-size `vector<int> freq(20001)` with `OFFSET = 10000`.
   - **Step 2:** Create buckets where `buckets[f]` stores all values appearing with frequency $f$.
   - **Step 3:** Iterate backwards from the maximum frequency $N$ down to $1$ and collect $K$ elements.
   - *Verdict:* Strictly $O(N)$ linear time, beating $O(N \log N)$ and eliminating all hash collision risks.

---

## 3. Complexity Analysis
Let $N = \text{nums.size()}$ and $V = 20,001$ (the bounded range $[-10^4, 10^4]$).

- **Time Complexity:** $O(N + V) \implies O(N)$
  - Frequency counting pass: $O(N)$ over input array.
  - Populating buckets: $O(V)$ scan across the bounded frequency array.
  - Collecting results from buckets: $O(N)$ worst-case scan across bucket lists until $K$ elements are accumulated.
  - Because $V = 20,001$ is a fixed constant, overall time is strictly **$O(N)$**.
- **Space Complexity:** $O(N + V) \implies O(N)$
  - Frequency array of fixed size $20,001$: $O(V)$.
  - Bucket lists hold at most $N$ unique elements: $O(N)$.
  - Output vector: $O(K)$.

---

## 4. Edge Cases & Gotchas
- [x] **Negative values:** Handled seamlessly via `OFFSET = 10000` mapping $[-10000, 10000] \rightarrow [0, 20000]$.
- [x] **$K$ equals array length ($K = N$):** All distinct elements are collected; loop terminates as soon as `result.size() == k`.
- [x] **Single-element array ($N = 1, K = 1$):** Immediately buckets at `buckets[1]` and returns.
- [x] **Tied frequencies:** The problem guarantees a unique answer; all ties at the boundary belong to the valid answer set.

---

## 5. Clean Code (Frequency Array + Bucket Sort)

```cpp
class Solution {
public:
    vector<int> topKFrequent(vector<int>& nums, int k) {
        constexpr int OFFSET = 10000;
        constexpr int RANGE = 20001;

        // 1. Count frequency using fixed array (avoids hash map overhead)
        vector<int> freq(RANGE);
        for (int num : nums) {
            ++freq[num + OFFSET];
        }

        // 2. Bucket by frequency: buckets[f] = numbers appearing exactly f times
        vector<vector<int>> buckets(nums.size() + 1);
        for (int i = 0; i < RANGE; ++i) {
            if (freq[i] > 0) {
                buckets[freq[i]].push_back(i - OFFSET);
            }
        }

        // 3. Collect from highest frequency downwards
        vector<int> result;
        result.reserve(k);

        for (int f = nums.size(); f >= 1 && result.size() < k; --f) {
            for (int num : buckets[f]) {
                result.push_back(num);
                if (result.size() == k) {
                    return result;
                }
            }
        }

        return result;
    }
};
```

---

## 6. Review & Takeaways

### Visualizing the Workflow

```text
nums = [1, 1, 1, 2, 2, 3], k = 2

1. Frequency Counting:
   1 -> 3
   2 -> 2
   3 -> 1

2. Bucket Inversion (Index = Frequency):
   Bucket[3]: [1]
   Bucket[2]: [2]
   Bucket[1]: [3]

3. Scan backwards from frequency 6 down to 1:
   f = 3 -> pick 1  (result: [1])
   f = 2 -> pick 2  (result: [1, 2], size == k -> return!)
```

---

### Alternative: Generic `unordered_map` + Bucket Sort (Unbounded Values)

If an interviewer removes the constraint on value bounds (e.g. `nums[i]` can be any 32-bit or 64-bit integer), switch Step 1 from a fixed array to `unordered_map<int, int>`:

```cpp
class Solution {
public:
    vector<int> topKFrequent(vector<int>& nums, int k) {
        // 1. Count frequency with hash map for unbounded input values
        unordered_map<int, int> count;
        for (int num : nums) {
            ++count[num];
        }

        // 2. Bucket sort by frequency (max frequency is always <= nums.size())
        vector<vector<int>> buckets(nums.size() + 1);
        for (auto& [num, freq] : count) {
            buckets[freq].push_back(num);
        }

        // 3. Collect top k
        vector<int> result;
        result.reserve(k);

        for (int f = nums.size(); f >= 1 && result.size() < k; --f) {
            for (int num : buckets[f]) {
                result.push_back(num);
                if (result.size() == k) return result;
            }
        }

        return result;
    }
};
```

---

### Comparison of All Approaches

| Approach | Time Complexity | Space Complexity | Pros & Cons |
| :--- | :---: | :---: | :--- |
| **Sort by Frequency** | $O(N \log N)$ | $O(N)$ | Fails the better-than-$O(N \log N)$ requirement. |
| **Min-Heap (`priority_queue`)** | $O(N \log K)$ | $O(N + K)$ | Good for data streams / small $K$, but has heap overhead. |
| **`unordered_map` + Bucket Sort** | $O(N)$ average | $O(N)$ | Generic, works for arbitrary numbers. |
| **Frequency Array + Bucket Sort (Optimal)** | **$O(N + V) = O(N)$** | **$O(N + V)$** | **Fastest on LeetCode constraints: zero hash collisions, cache friendly.** |

---

### C++ Interview Takeaway

> *"When frequencies or values are bounded, avoid comparison-based sorting ($O(N \log N)$) and heaps ($O(N \log K)$) — use **Bucket Sort** to achieve strictly linear $O(N)$ time."*

* **Next Review Date:** Medium priority (classic bucket sort paradigm).
* **Key Takeaway:** The maximum frequency of any element in an array of size $N$ cannot exceed $N$. Using frequency as an array index (`buckets[f]`) guarantees an $O(N)$ reverse-order collection.
