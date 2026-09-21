# 0128. Longest Consecutive Sequence

- **Problem Link:** https://leetcode.com/problems/longest-consecutive-sequence/
- **Difficulty:** `Medium`
- **NeetCode Category:** `Arrays & Hashing`
- **LeetCode Topics:** `Array` / `Hash Table` / `Union-Find`
- **Core Pattern:** `Hash Set + Sequence Start Detection (!set.count(num - 1))`
- **Last Practiced:** 2026-09-19
- **Proficiency Level:** 
  - [x] Level 1: Solved smoothly (< 20 mins, optimal)
  - [ ] Level 2: Struggled / Non-optimal / Edge-case bugs
  - [ ] Level 3: Needed editorial or hints

---

## 1. Pattern Recognition & Triggers
- Clues in prompt: *"Given an unsorted array of integers nums"*, *"return the length of the longest consecutive elements sequence"*, *"You must write an algorithm that runs in O(n) time"*.
- Core intuition: The $O(n)$ requirement strictly forbids comparison-based sorting ($O(n \log n)$). Consecutive numbers differ by exactly $1$ ($x, x+1, x+2, \dots$). If we put all elements in an `unordered_set`, we can look up neighboring numbers in average $O(1)$ time. Crucially, to prevent recounting the same sequence over and over, we only expand forward from **sequence starters** — numbers where `num - 1` does NOT exist in the set.

---

## 2. Approach & Trade-offs

1. **Approach 1 — Sorting ($O(N \log N)$):**
   - Sort the array and scan linearly to count consecutive streaks, skipping duplicates.
   - *Verdict:* Trivial to write, but violates the explicit $O(N)$ runtime constraint demanded by the problem description.

2. **Approach 2 — Naive Hash Set Expansion ($O(N^2)$ worst case):**
   - Insert all numbers into a hash set. For every element `num`, expand both left (`num - 1`) and right (`num + 1`).
   - *Verdict:* Redundantly traverses segments of the same consecutive streak for every member, leading to quadratic worst-case runtime.

3. **Approach 3 — Hash Set + Sequence-Start Detection (Optimal & Implemented):**
   - Insert all elements into an `unordered_set<int> numSet`.
   - Iterate over unique values in `numSet`.
   - Check if `num - 1` exists:
     - If `numSet.find(num - 1) != numSet.end()`: `num` is in the middle of an already tracked sequence $\rightarrow$ **skip immediately (`continue`)**.
     - If `num - 1` is absent: `num` is guaranteed to be the **absolute start of a sequence** $\rightarrow$ expand forward (`num + 1`, `num + 2`, ...) using a `while` loop.
   - *Verdict:* Each distinct element is visited at most twice across the entire algorithm, ensuring strictly $O(N)$ total time complexity.

---

## 3. Complexity Analysis

- **Time Complexity:** $O(N)$ average
  - Building the `unordered_set`: $O(N)$ average time.
  - Outer loop + sequence-start check: runs once per unique number $\rightarrow O(N)$ average $O(1)$ lookups.
  - Inner `while` loop: only executes for elements that are sequence starters. Because every consecutive sequence is traversed from its first element to its end exactly once, the inner loop advances at most $N$ times across the entire execution of the program.
  - Amortized / Total Time: $O(N) + O(N) = O(N)$.
- **Space Complexity:** $O(N)$
  - The `unordered_set` stores $U$ unique elements where $U \le N \le 10^5$.

---

## 4. Edge Cases & Gotchas
- [x] **Empty array (`nums = []`):** Handled gracefully; the loop does not run and returns `longest = 0`.
- [x] **Single element (`nums = [7]`):** Sequence length is $1$, correctly returned.
- [x] **Duplicate elements (`nums = [1, 2, 0, 1]`):** Iterating through `numSet` (`for (int num : numSet)`) instead of `nums` automatically strips duplicates upfront, preventing repeated checks.
- [x] **Negative numbers & large ranges:** Handled naturally by standard integer hash functions.

---

## 5. Clean Code (Optimal Solution: unordered_set + Sequence-Start Detection)

```cpp
class Solution {
public:
    int longestConsecutive(vector<int>& nums) {
        unordered_set<int> numSet(nums.begin(), nums.end());
        int longest = 0;

        for (int num : numSet) {
            // If num - 1 exists, num is NOT the beginning of a sequence -> skip
            if (numSet.find(num - 1) != numSet.end()) {
                continue;
            }

            // num is the true start of a streak -> expand forward
            int length = 1;
            while (numSet.find(num + length) != numSet.end()) {
                ++length;
            }

            longest = max(longest, length);
        }

        return longest;
    }
};
```

---

## 6. Review & Takeaways

### Visualizing the Sequence-Start Filter

Given `nums = [100, 4, 200, 1, 3, 2]`:

```text
numSet = {100, 4, 200, 1, 3, 2}

Element    Is (num - 1) present?    Decision    Sequence Formed
---------------------------------------------------------------------
100        99 present? No           START       100 (len 1)
4          3 present? Yes           SKIP        -
200        199 present? No          START       200 (len 1)
1          0 present? No            START       1 -> 2 -> 3 -> 4 (len 4)
3          2 present? Yes           SKIP        -
2          1 present? Yes           SKIP        -
```

Result: `longest = max(1, 1, 4) = 4`. The sequence `[1, 2, 3, 4]` was traversed exactly once.

---

### Interview Pitch: *"Why is a nested while loop inside a for loop O(n)?"*

> *"At first glance, a while loop inside a for loop looks like $O(N^2)$. However, the condition `if (numSet.find(num - 1) != numSet.end()) continue;` acts as a strict guard. The inner while loop only triggers for the unique head of each consecutive chain. Non-starting elements are discarded in $O(1)$ time. Because each number in the dataset can belong to only one sequence, each element is touched at most twice across the entire algorithm: once when tested in the outer loop, and once when enumerated in the inner while loop. Therefore, the total number of operations is bounded by $2N$, achieving strict $O(N)$ runtime."*

---

### The Core Architectural Pattern

```text
Longest Consecutive Sequence
         ↓
Insert into unordered_set
         ↓
Iterate unique elements: Is (num - 1) in set?
     ↙                    ↘
  Yes                      No (Found Sequence Head!)
   ↓                        ↓
  Skip (O(1))              Expand forward (num + 1, num + 2, ...)
                            ↓
                           Update longest = max(longest, length)
```

* **Next Review Date:** Low priority (benchmark sequence-start pattern mastered).
* **Key Takeaway:** When searching for global chains in an unordered collection in $O(N)$ time, convert the collection to a hash set and anchor searches exclusively at the canonical beginning of each chain (`num - 1` absent).
