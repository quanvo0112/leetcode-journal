# 0001. Two Sum

- **Problem Link:** https://leetcode.com/problems/two-sum/
- **Difficulty:** `Easy`
- **NeetCode Category:** `Arrays & Hashing`
- **LeetCode Topics:** `Array` / `Hash Table`
- **Core Pattern:** `One-pass Hash Map (Complement Lookup)`
- **Last Practiced:** 2026-09-17
- **Proficiency Level:**
  - [x] Level 1: Solved smoothly (< 20 mins, optimal)
  - [ ] Level 2: Struggled / Non-optimal / Edge-case bugs
  - [ ] Level 3: Needed editorial or hints

---

## 1. Pattern Recognition & Triggers
- Clues in prompt: *"add up to target"*, *"return indices"*, *"only one valid answer exists"*.
- Core intuition: We need to find if a matching pair exists for each element: $\text{complement} = \text{target} - \text{current\_val}$. Using a **Hash Map** (`value -> index`) gives $O(1)$ lookup time for the complement.

---

## 2. Approach & Trade-offs
1. **Brute Force:** Check every pair $(i, j)$ where $i \ne j$ with nested loops $\rightarrow$ Time: $O(N^2)$, Space: $O(1)$. Triggers TLE for large inputs ($N = 10^5$).
2. **Sort + Two Pointers:** Sort array and use left/right pointers $\rightarrow$ Time: $O(N \log N)$, Space: $O(N)$ (requires storing original indices `pair<value, index>`). Slower than hash map and loses original index positioning.
3. **One-Pass Hash Map (Optimal):**
   - Initialize an empty hash map `prevMap` storing `{number: index}`.
   - For each element `nums[i]`, compute `complement = target - nums[i]`.
   - If `complement` exists in `prevMap`, return `{prevMap[complement], i}`.
   - Otherwise, record `prevMap[nums[i]] = i` and continue.

---

## 3. Complexity Analysis
- **Time Complexity:** $O(N)$ — Single pass through the array; hash map operations operate in $O(1)$ average time.
- **Space Complexity:** $O(N)$ — In the worst-case scenario (matching pair at the very end), the hash map holds up to $N - 1$ entries.

---

## 4. Edge Cases & Gotchas
- [x] Duplicate values (e.g., `nums = [3, 3]`, `target = 6`): The first `3` is looked up (not found) and stored at index `0`. When the second `3` arrives, `target - 3 = 3` matches the stored key, correctly returning `{0, 1}`.
- [x] Negative values: Negative numbers and negative targets are handled transparently by arithmetic.
- [x] Preventing self-matching: Searching the map *before* inserting `nums[i]` guarantees that an element cannot pair with itself ($i \ne j$).

---

## 5. Clean Code (Submitted Solution)

```cpp
class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        unordered_map<int, int> prevMap;

        for (int i = 0; i < nums.size(); ++i) {
            int complement = target - nums[i];

            if (prevMap.find(complement) != prevMap.end()) {
                return {prevMap[complement], i};
            }

            prevMap[nums[i]] = i;
        }

        return {};
    }
};
```

---

## 6. Review & Takeaways

### Better Implementation: Single Lookup & Reserve

In the submitted solution:
```cpp
if (prevMap.find(complement) != prevMap.end()) {
    return {prevMap[complement], i}; // Triggers a second hash computation & lookup
}
```
`prevMap` is queried **twice** for the same key: once in `find()` and once in `operator[]`. We can optimize this into a **single lookup** by storing the iterator from `find()`:

```cpp
class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        unordered_map<int, int> prevMap;
        // Optional: Pre-allocate bucket count to eliminate rehashing overhead
        prevMap.reserve(nums.size());

        for (int i = 0; i < nums.size(); ++i) {
            int complement = target - nums[i];

            auto it = prevMap.find(complement);
            if (it != prevMap.end()) {
                return {it->second, i}; // Single lookup via iterator
            }

            prevMap[nums[i]] = i;
        }

        return {};
    }
};
```

---

### C++ Interview Deep Dive

#### 1. Why `unordered_map` over `map`?
- **`unordered_map`:** Built on a Hash Table $\rightarrow$ **Average $O(1)$** lookup and insertion. Since Two Sum does not require sorted keys, this is optimal.
- **`map`:** Built on a Red-Black Tree (Self-balancing BST) $\rightarrow$ **Strict $O(\log N)$** operations.

#### 2. Interview Question: *"Is `unordered_map` always $O(1)$?"*
- **No.** Average-case lookup/insert is $O(1)$, but in the worst case (excessive hash collisions mapping many keys into the same bucket), operations degrade to **$O(N)$**, resulting in an overall $O(N^2)$ runtime.

#### 3. Why Iterate Once and Check *Before* Inserting?
- Doing a single pass and checking before inserting serves two crucial purposes:
  1. Handles duplicate pairs (e.g., `[3, 3]`, `target = 6`) naturally without collisions overwriting the key prematurely.
  2. Automatically prevents self-matching ($i \neq j$) because `nums[i]` is not in the map when we search for its complement.

---

### Comparison Summary

| Approach | Time Complexity | Space Complexity | Notes |
| :--- | :---: | :---: | :--- |
| **Brute Force** | $O(N^2)$ | $O(1)$ | Simple nested loops, TLE on large arrays |
| **Sort + Two Pointers** | $O(N \log N)$ | $O(N)$ | Requires tracking original indices `pair<val, idx>` |
| **`unordered_map` (Optimal)** | **Average $O(N)$** | **$O(N)$** | **Most direct, optimal for interviews** |

* **Next Review Date:** Low priority (benchmark pattern mastered).
* **Key Takeaway:** Formulate pair search as $\text{complement} = \text{target} - \text{nums}[i]$. Always use iterator-based access (`it->second`) to eliminate redundant hash lookups.
