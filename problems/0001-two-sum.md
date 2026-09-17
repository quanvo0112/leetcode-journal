# 0001. Two Sum

- **Problem Link:** https://leetcode.com/problems/two-sum/
- **Difficulty:** `Easy`
- **Topic / Pattern:** `Array` / `Hash Table`
- **Last Practiced:** 2026-09-17
- **Proficiency Level:** 
  - [x] 🟢 Level 1: Solved smoothly (< 20 mins, optimal)
  - [ ] 🟡 Level 2: Struggled / Non-optimal / Edge-case bugs
  - [ ] 🔴 Level 3: Needed editorial or hints

---

## 1. Pattern Recognition & Triggers
- Clues in prompt: *"add up to target"*, *"return indices"*, *"only one valid answer exists"*.
- Core intuition: We need to find if a matching pair exists for each element: $\text{complement} = \text{target} - \text{current\_val}$. Using a **Hash Map** (`value -> index`) gives $O(1)$ lookup time for the complement.

---

## 2. Approach & Trade-offs
1. **Brute Force:** Check every pair $(i, j)$ where $i \ne j$ with nested loops $\rightarrow$ Time: $O(N^2)$, Space: $O(1)$. Exceeds optimal limits for large inputs.
2. **Two Pointers (After Sorting):** Sort array and use left/right pointers $\rightarrow$ Time: $O(N \log N)$, Space: $O(N)$ (storing original indices). Feasible, but slower than hash map and requires tracking original indices.
3. **One-Pass Hash Map (Optimal):**
   - Initialize an empty hash map `prevMap` storing `{number: index}`.
   - For each element `nums[i]`, compute `complement = target - nums[i]`.
   - If `complement` exists in `prevMap`, return `{prevMap[complement], i}`.
   - Otherwise, record `prevMap[nums[i]] = i` and continue.

---

## 3. Complexity Analysis
- **Time Complexity:** $O(N)$ — We traverse the array once; hash map lookups and insertions operate in $O(1)$ average time.
- **Space Complexity:** $O(N)$ — In the worst case, the hash map holds up to $N - 1$ key-value pairs before locating the answer on the final element.

---

## 4. Edge Cases & Gotchas
- [x] Duplicate values (e.g., `nums = [3, 3]`, `target = 6`): The first `3` is looked up, but not found in the map initially. When the second `3` is reached, `target - 3 = 3` matches the first index already inserted.
- [x] Negative values: Negative integers and negative targets are handled directly by arithmetic without special branches.
- [x] Reusing the same index: Searching the map *before* adding the current element guarantees index $i \ne j$.

---

## 5. Clean Code

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

* *Next Review Date:* Low priority (benchmark problem).
* *Key Takeaway:* Transform a pair-matching problem from "finding $A + B = C$" to "looking up $C - A$ in a lookup table." The one-pass hash map simultaneously prevents self-matching and reduces overall passes.

