# 0242. Valid Anagram

- **Problem Link:** https://leetcode.com/problems/valid-anagram/
- **Difficulty:** `Easy`
- **NeetCode Category:** `Arrays & Hashing`
- **LeetCode Topics:** `Hash Table` / `String` / `Sorting`
- **Core Pattern:** `Fixed Frequency Array (array<int, 26>) Counting`
- **Last Practiced:** 2026-09-17
- **Proficiency Level:** 
  - [x] Level 1: Solved smoothly (< 20 mins, optimal)
  - [ ] Level 2: Struggled / Non-optimal / Edge-case bugs
  - [ ] Level 3: Needed editorial or hints

---

## 1. Pattern Recognition & Triggers
- Clues in prompt: *"t is an anagram of s"*, *"lowercase English letters"*.
- Core intuition: An anagram requires matching character frequencies. When input is constrained to a fixed alphabet (`'a'` through `'z'`), an indexed integer array `count[26]` outperforms dynamic hash structures.

---

## 2. Approach & Trade-offs
1. **Sorting:** Sort both strings and compare `s == t` $\rightarrow$ Time: $O(N \log N)$, Space: $O(1)$ or $O(N)$. Simple to implement, but slower execution.
2. **Fixed-Size Frequency Array (Implemented):**
   - Check `s.length() != t.length()`; return `false` immediately if lengths differ.
   - Maintain `int count[26] = {0}`.
   - In a single pass, increment frequency for `s[i]` and decrement for `t[i]`.
   - Iterate through the 26-element array to ensure all values returned to 0.
3. **Follow-up (Unicode handling):**
   - Fixed 26-element indexing does not support variable-width encodings.
   - Replace the array with `unordered_map<char32_t, int>` or `unordered_map<wchar_t, int>`.

---

## 3. Complexity Analysis
- **Time Complexity:** $O(N)$ — Where $N$ is the length of string $s$. Requires a single pass of length $N$, followed by checking a constant 26 buckets.
- **Space Complexity:** $O(1)$ — Storage is fixed to an array of size 26 regardless of input size $N$.

---

## 4. Edge Cases & Gotchas
- [x] Different string lengths: Caught immediately via guard clause.
- [x] Single-character strings: Evaluates correctly without indexing issues.
- [x] Character offset mapping: `char - 'a'` safely maps `'a'...'z'` to range `0...25`.

---

## 5. Source Code (Submitted Solution)

```cpp
class Solution {
public:
    bool isAnagram(string s, string t) {
        if (s.length() != t.length()) {
            return false;
        }

        int count[26] = {0};

        for (int i = 0; i < s.length(); ++i) {
            count[s[i] - 'a']++;
            count[t[i] - 'a']--;
        }

        for (int val : count) {
            if (val != 0) {
                return false;
            }
        }

        return true;
    }
};
```

---

## 6. Review & Takeaways

### Optimization / Alternative: Early-Exit Pass

Instead of running a second loop over the 26-element array at the end, populate counts for `s` first, then decrement against `t`. If any bucket drops below zero, terminate immediately:

```cpp
class Solution {
public:
    bool isAnagram(string s, string t) {
        if (s.length() != t.length()) return false;

        int count[26] = {0};

        for (char c : s) {
            count[c - 'a']++;
        }

        for (char c : t) {
            if (--count[c - 'a'] < 0) {
                return false; // Early exit: found mismatched frequency mid-iteration
            }
        }

        return true;
    }
};
```

* **Next Review Date:** Low priority (standard frequency counting pattern mastered).
* **Key Takeaway:** A 26-element integer buffer provides $O(1)$ auxiliary space and cache-friendly execution. Adding an early-exit check inside the decrement phase skips unnecessary loop cycles on mismatched strings.
