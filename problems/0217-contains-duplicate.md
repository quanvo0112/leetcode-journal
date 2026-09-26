# 0217. Contains Duplicate

- **Problem Link:** https://leetcode.com/problems/contains-duplicate/
- **Difficulty:** `Easy`
- **NeetCode Category:** `Arrays & Hashing`
- **LeetCode Topics:** `Array` / `Hash Table` / `Sorting`
- **Core Pattern:** `Hash Set Lookup`
- **Last Practiced:** 2026-09-26
- **Proficiency Level:**
  - [x] Level 1: Solved smoothly (< 20 mins, optimal)
  - [ ] Level 2: Struggled / Non-optimal / Edge-case bugs
  - [ ] Level 3: Needed editorial or hints

---

## 1. Pattern Recognition & Triggers
- Clues in prompt: *"appears at least twice"*, *"distinct"*.
- Core intuition: Need to verify if an element has already been seen with an average $O(1)$ lookup time $\rightarrow$ Use a **Hash Set**.

---

## 2. Approach & Trade-offs
1. **Brute Force:** Nested loops comparing all pairs $\rightarrow$ Time: $O(N^2)$, Space: $O(1)$. Triggers TLE for $N = 10^5$.
2. **Sorting:** Sort array first, then check adjacent pairs `nums[i] == nums[i-1]` $\rightarrow$ Time: $O(N \log N)$, Space: $O(1)$ to $O(N)$ depending on sorting algorithm.
3. **Hash Set (Optimal):**
   - Initialize an empty hash set (`unordered_set<int> seen`).
   - Iterate through `nums`. If `num` exists in `seen`, return `true` immediately (early return).
   - Otherwise, insert `num` into `seen`.
   - Return `false` if loop finishes without duplicates.

---

## 3. Complexity Analysis
- **Time Complexity:** $O(N)$ — Single pass through the array; hash set operations (`insert`, `find`) take $O(1)$ average time.
- **Space Complexity:** $O(N)$ — In the worst-case scenario (all distinct elements), the set stores up to $N$ integers.

---

## 4. Edge Cases & Gotchas
- [x] Single-element array: The loop executes once and correctly returns `false` without out-of-bound errors.
- [x] Negative numbers: Handled automatically by hash function.
- **C++ Tip:** Avoid `set` here unless ordered elements are required, because `set` uses a balanced BST ($O(\log N)$ operations) instead of a hash table ($O(1)$ average).

---

## 5. Clean Code

```cpp
class Solution {
public:
    bool containsDuplicate(vector<int>& nums) {
        unordered_set<int> seen;

        for (int num : nums) {
            if (seen.find(num) != seen.end()) {
                return true;
            }
            seen.insert(num);
        }

        return false;
    }
};
```

---

## 6. Review & Takeaways

* *Next Review Date:* Low priority (foundational pattern).
* *Key Takeaway:* Whenever a problem asks for duplicate detection or presence checking in an unsorted collection, consider a hash set first.
